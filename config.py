import os


class Config:

    '''
    General configuration parent class

    '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):

    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevConfig(Config):

    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://hannahnjoroge:password@localhost/covidstats'
    SECRET_KEY = 'kfgkgkjlkndlclkdslkcndslkvndsvdvuds'
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
}
