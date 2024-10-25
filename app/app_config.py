from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1985@localhost/faculty_db"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dsggdtwp#e34d[f2fl2'
    SECURITY_PASSWORD_SALT = 'fdagsksp33r5wtssgksghpdh'
    SECURITY_REGISTERABLE =  True
    SECURITY_SEND_REGISTER_EMAIL = False


app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app=app, session_options={'autoflush' : False})