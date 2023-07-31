import os

class Config:
 DEBUG = False
 DEVELOPMENT = False
 CSRF_ENABLED = True
 ASSETS_DEBUG = False
 SECRET_KEY = os.environ.get('SECRET_KEY')

class ProductionConfig(Config):
 pass

class DevelopmentConfig(Config): 
 DEBUG = True
 DEVELOPMENT = True
 TEMPLATES_AUTO_RELOAD = True
 ASSETS_DEBUG = True
 SECRET_KEY = 'thisisatestsecretkey'
