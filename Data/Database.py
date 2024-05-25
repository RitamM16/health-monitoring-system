from flask import Flask
from config import MYSQL_CONN_STRING, MYSQL_CELERY_CONN_STRING
from sqlalchemy_utils import database_exists, create_database
from Data.Models import db

def initSQLAlchemy(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_CONN_STRING
    
    if not database_exists(MYSQL_CONN_STRING):
        create_database(MYSQL_CONN_STRING)
        
    if not database_exists(MYSQL_CELERY_CONN_STRING):
        create_database(MYSQL_CELERY_CONN_STRING)
    
    with app.app_context():
        db.init_app(app)
        db.create_all()
    
    return db