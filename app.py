from datetime import datetime
from enum import Enum

from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

from config import cfg, secret, domain
from core import base10to62

app = Flask(__name__)
app.config.from_object(cfg)
db = SQLAlchemy(app)


class Short(db.Model):
    __tablename__ = 'short'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    url = db.Column(db.VARCHAR(256), nullable=False)
    code = db.Column(db.VARCHAR(10), unique=True, index=True)
    type = db.Column(db.CHAR(6), nullable=False, default='system')
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'Short(id={self.id}, url={self.url}, code={self.code}, type={self.type})'


class ShortType(Enum):
    System = 'system'
    Custom = 'custom'


class Code(Enum):
    OK = 0  # 请求成功
    InvalidRequest = 10000  # 请求数据非法


class Response:
    """通用 HTTP Response，code 为 0 时代表请求成功，此时 data 有效
    code 为非 0 时代表请求失败，此时 error 有效
    """

    def __init__(self, code: Code, data=None, error=None) -> None:
        super().__init__()
        self.code = code
        self.data = data
        self.error = error

    def build(self):
        from flask import jsonify
        from flask import make_response
        resp = jsonify({
            'code': self.code.value,
            'data': self.data,
            'error': self.error
        })
        return make_response(resp, 200)

    def __repr__(self):
        return f'Response(code={self.code}, data={self.data}, error={self.error})'


cfg.init_app(app)
db.init_app(app)
db.create_all()


@app.route('/')
def index():
    return 'hello!'


@app.route('/404')
def error_404():
    return 'Unknown code!'


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
            return Response(Code.OK, data=domain + code).build()
    else:
        # Use system generated shorten code
        short = Short(url=url, type=ShortType.System.value)
        db.session.add(short)
        db.session.commit()

        # Generate shorten code using id
        code = base10to62(short.id, secret)

        # Judge generated code exist or not
        recheck_count = 0
        while exist := Short.query.filter_by(code=code).scalar():
            if recheck_count >= 5:
                return Response(Code.InvalidRequest, 'System Error! Please try later').build()
            else:
                # If exist, regenerate using exist id, the reason is that only customized code will
                # cause conflict with auto-generated code. And the id of customized code's record
                # has not been used to generate code.
                code = base10to62(exist.id, secret)
                recheck_count += 1

        # Update short table
        short.code = code
        db.session.add(short)
        db.session.commit()
        return Response(Code.OK, data=domain + code).build()


@app.route('/<code>', methods=['GET', 'POST'])
def decode(code):
    if not code:
        return Response(Code.InvalidRequest, error='Request param invalid!').build()
    short = Short.query.filter_by(code=code).scalar()
    if not short:
        return redirect('/404', code=302)
    else:
        return redirect(short.url, code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
