from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

from config import cfg
from core import base10to62
from models import *

db = SQLAlchemy()
app = Flask(__name__)

app.config.from_object(cfg)
cfg.init_app(app)
db.init_app(app)


@app.route('/')
def index():
    db.create_all()
    return 'hello!'


@app.route('/encode', methods=['POST'])
def encode():
    if not request.json:
        return Response(Code.InvalidRequest, error='Request MIME type must be json').build()
    url, code = request.json.get('url'), request.json.get('code')
    if not url:
        return Response(Code.InvalidRequest, error='Source url is required!').build()
    if code:
        # If user choose to customize shorten code, check code exist or not
        short = Short.query.filter_by(code=code).scalar()
        if short:
            return Response(code=Code.InvalidRequest, error='Code already exist!').build()
        else:
            # If code does not exist
            short = Short(url=url, code=code, type=ShortType.Custom.value)
            db.session.add(short)
            db.session.commit()
            return Response(Code.OK, data=code).build()
    else:
        # Use system generated shorten code
        short = Short(url=url, type=ShortType.System.value)
        db.session.add(short)
        db.session.commit()

        # Generate shorten code using id
        code = base10to62(short.id)

        # Judge generated code exist or not
        exist = Short.query.filter_by(code=code).scalar()
        if exist:
            # If exist, regenerate using exist id, the reason is that only customized code will
            # cause conflict with auto-generated code. And the id of customized code's record
            # has not been used to generate code.
            code = base10to62(exist.id)

        # Update short table
        short.code = code
        db.session.add(short)
        db.session.commit()
        return Response(Code.OK, data=code).build()


@app.route('/decode', methods=['POST'])
def decode():
    if not request.json:
        abort('Request MIME type must be json')
    code = request.json.get('code')
    if not code:
        return Response(Code.InvalidRequest, error='JSON data invalid!').build()
    short = Short.query.filter_by(code=code).scalar()
    if not short:
        return Response(Code.InvalidRequest, error='No such code!').build()
    return Response(Code.OK, data={'url': short.url}).build()


if __name__ == '__main__':
    app.run()
