from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
from flask_login import LoginManager
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4" % quote('cun112004')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3
app.secret_key='dkfd'
db = SQLAlchemy(app=app)
login = LoginManager(app=app)