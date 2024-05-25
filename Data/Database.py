from flask import Flask
from config import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER, MYSQL_DATABASE
from sqlalchemy_utils import database_exists, create_database
from Data.Models import db

MYSQL_CONN_STRING = f'mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

def initSQLAlchemy(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_CONN_STRING
    
    if not database_exists(MYSQL_CONN_STRING):
        create_database(MYSQL_CONN_STRING)
    
    with app.app_context():
        db.init_app(app)
        db.create_all()
    
    return db