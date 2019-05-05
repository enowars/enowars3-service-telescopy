from flask import Flask
from flask import jsonify 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planets.db'
db = SQLAlchemy(app)
CORS(app)