from datetime import datetime
from enum import Enum

from app import db


class Short(db.Model):
    __tablename__ = 'short'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    url = db.Column(db.VARCHAR(256), nullable=False)
    code = db.Column(db.VARCHAR(10), unique=True)
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
    NotFound = 10001  # HTTP 404 错误
    InternalError = 10002  # HTTP 500 错误

    UsernameRegistered = 20000  # 用户名已被注册
    UserNotExist = 200001  # 用户不存在

    RequestFailed = 99999  # 请求失败


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
