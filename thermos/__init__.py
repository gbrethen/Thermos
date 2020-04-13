import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = b'j\xd3|\x7fb\xc4\x9b\x9e\x90Q\xab\xdb\x0e\xe1S)m{\xf3\t\xaf\xaa{\x9d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True

db = SQLAlchemy(app)

import thermos.models
import thermos.views