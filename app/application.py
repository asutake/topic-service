from flask import Flask
from app import config
from sqlalchemy.pool import QueuePool
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# SQLAlchemy
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
        **{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost:3306'),
            'database': os.getenv('DB_DATABASE', 'topic'),
        })
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': False,
}

db = SQLAlchemy(app, session_options={
    'autocommit': False,
})
m = Migrate(app, db)
