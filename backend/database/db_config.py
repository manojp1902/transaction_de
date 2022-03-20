from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma=None
def initialize_db(app):
    db.init_app(app)
    
from flask_marshmallow import Marshmallow
def initialise_marshmallow(app):
    global ma
    ma= Marshmallow(app)
    