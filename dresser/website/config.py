import os
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
DB_NAME = 'database.db'

class Config:
 DEBUG = False
 DEVELOPMENT = False
 CSRF_ENABLED = True
 ASSETS_DEBUG = False
 SECRET_KEY = os.environ.get(SECRET_KEY)
 SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'

class ProductionConfig(Config):
 pass

class DevelopmentConfig(Config): 
 DEBUG = True
 DEVELOPMENT = True
 TEMPLATES_AUTO_RELOAD = True
 ASSETS_DEBUG = True
 SECRET_KEY = 'thisisatestsecretkey'
 SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
