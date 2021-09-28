import os
class Config:

    '''
    General configuration parent class
    
    '''

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'kfgkgkjlkndlclkdslkcndslkvndsvdvuds'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost/create_api'


class ProdConfig(Config):

    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True



config_options = {

    'development':DevConfig,
    'production':ProdConfig,
} 