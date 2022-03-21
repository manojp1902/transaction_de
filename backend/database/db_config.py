from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # new
db = SQLAlchemy()
ma = Marshmallow()
def initialize_db(app):
    db.init_app(app)
    
from flask_marshmallow import Marshmallow
def initialise_marshmallow(app):
    
    ma.init_app(app)
    