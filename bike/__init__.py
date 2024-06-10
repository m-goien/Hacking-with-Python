from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bikeuser:example123@192.168.178.100/bikedb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bikeuser:example123@141.87.56.33/bikedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'f1c50cdf58a5ac7024799454'

db = SQLAlchemy(app)

from bike import routes
