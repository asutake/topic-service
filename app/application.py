from flask import Flask
from app import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
