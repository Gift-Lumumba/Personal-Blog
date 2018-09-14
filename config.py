import os

class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://gift:gL0711@localhost/blog'

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True



class ProdConfig(Config):
    pass


class DevConfig(Config):
    pass

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}