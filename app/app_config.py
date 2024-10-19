from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1985@localhost/faculty_db"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dsggdtwp#e34d[f2fl2'


app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app=app, session_options={'autoflush' : False})