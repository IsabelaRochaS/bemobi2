"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
 
from Bemobi2.views import view
app.register_blueprint(view)
 
db.create_all()
import Bemobi2.views
