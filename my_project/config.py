import os

DEBUG = True

#需要用到session，所以
SECRET_KEY = os.urandom(24)

#需要用到数据库，所以
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'QA_demo'
USERNAME = 'root'
PASSWORD = 'xudaqiang'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False