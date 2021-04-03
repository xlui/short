import datetime
import os
import sys

work_dir = os.path.dirname(os.path.abspath(__file__))
env = os.environ.get('ENV') or 'default'
secret = os.environ.get('SECRET') or 'PnX6DWihwH8OAJklcaq9UVzNedBpSI3yCvMfbjstLZG7oK5YT2rEx01QmF4uRg'
# check secret
if len(secret) != 62 or len(set(secret)) != 62:
    print(f'SECRET is invalid. secret:{secret}')
    sys.exit(1)
domain = os.environ.get('DOMAIN') or 'http://127.0.0.1:5000/'
if not domain:
    print(f'DOMAIN is invalid. domain:{domain}')
    sys.exit(1)
if not domain.endswith('/'):
    print(f'DOMAIN should ends with "/". domain:{domain}')
    sys.exit(1)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=7)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(work_dir, "data-dev.sqlite")}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(work_dir, "data-test.sqlite")}'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(work_dir, "data.sqlite")}'


__cfgs = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,

    'default': DevelopmentConfig
}
cfg = __cfgs[env]
