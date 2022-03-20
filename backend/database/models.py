
from .db_config import db
from .db_config import ma
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False,default=2)
    ts = db.Column(db.DateTime, nullable = False,
                     default = datetime.datetime.now) 
    transaction_amt = db.Column(db.Float, nullable = False,default=1000)
    def __init__(self,user_id,txn_amnt):
        self.user_id=user_id
        self.transaction_amt=txn_amnt
     



class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Float,nullable= False,)
                     
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('user_id','ts','transaction_amount')

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
   


    # def hash_password(self):
    #     self.password = generate_password_hash(self.password).decode('utf8')

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)
    
    # def update_time(self):
    #     self.last_login = self.current_login
    #     self.current_login = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    #     # print("Update time time {}".format)

# class UserGists(db.DynamicDocument):
#     meta = {'collection' : 'user_gists'}
#     id = db.StringField(primary_key=True)

#d.strftime('%Y-%m-%dT%H:%M:%SZ')
#datetime.strptime("2001-2-3 10:11:12", "%Y-%m-%d %H:%M:%S")