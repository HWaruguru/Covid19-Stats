import os
class Config:

    '''
    General configuration parent class
    
    '''

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost/created_api'

    SECRET_KEY = 'kfgkgkjlkndlclkdslkcndslkvndsvdvuds'



class ProdConfig(Config):

    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


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