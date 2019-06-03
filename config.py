import datetime
import os

work_dir = os.path.abspath(os.curdir)
env = os.environ.get('ENV') or 'default'


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
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
cfg = __cfgs[env]
