
from .db_config import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class UsersDB(db.DynamicDocument):
    meta = { 'collection' : 'users_db' }
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6) 
    last_login = db.DateTimeField()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def update_time(self):
        
        self.last_login = datetime.datetime.utcnow()
        # print("Update time time {}".format)

class UserGists(db.DynamicDocument):
    meta = {'collection':'user_gists'}
#d.strftime('%Y-%m-%dT%H:%M:%SZ')
#datetime.strptime("2001-2-3 10:11:12", "%Y-%m-%d %H:%M:%S")