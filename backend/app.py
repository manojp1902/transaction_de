import mimetypes
from urllib import response
from flask import Flask, request,render_template , make_response, redirect,url_for
from flask_restful import Resource, Api,reqparse
import flask
import json
import datetime
from flask.json import jsonify
from database.db_config import initialize_db, initialise_marshmallow
from sqlalchemy import create_engine

import  datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import json
import os
from pathlib import Path

app = Flask(__name__,template_folder='templates')
engine = create_engine('sqlite:///test.db')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
# jwt = JWTManager(app)


initialize_db(app)
initialise_marshmallow(app)
# initialise_marshmallow(app)
from database.models import Transaction,Balance
from database.db_config import db
from flask_migrate import Migrate
with app.app_context():
    db.create_all()


# db.session.commit()
    
#flask-restful framework`
api = Api(app)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()


# class SignupApi(Resource):
#     def post(self):
#         #issue: request.get_json works for postman not for html form
#         # body = request.get_json(force=True)
#         print(request.form.get('username'))
#         user = UsersDB(username=request.form.get('username'),
#                         password=request.form.get('password'),
#                         api_token = request.form.get('api_token'),
#                         company_domain=request.form.get('company_domain'))
#         user.hash_password()
#         user.save()
#         id = user.id
#         return {'id': str(id)}, 201
    
#     def get(self):
#         #add headers to avoid displaying only text in browser
#         headers = {'Content-Type': 'text/html','Access-Control-Allow-Origin':'*'}
#         return make_response(render_template('index.html'))

# class LoginApi(Resource):
#     def post(self):
        
#         user = UsersDB.objects.get(username=request.form.get('username'))
#         authorized = user.check_password(password=request.form.get('password'))

        

#         if not authorized:
#             return {'message': 'Email or password invalid'}, 401
#         else:
#             last_login = user['last_login']
#             user.update_time()
#             user.save()
#             expires = datetime.timedelta(minutes=10)
#             access_token = create_access_token(identity = str(user.id), 
#                                             expires_delta = expires)
    
#             return {'message': 'User successfully authenticated',
#                     "last_login": str(last_login),
#                     'token': access_token
#                      },201
#             # flask.redirect(flask.url_for('latestgists'), code=307)
        
#     def get(self):
#         return make_response(render_template('login.html')) 
    
# class LatestGists(Resource):
#     #cannot run background task for specific user , update for all users in database
#     @jwt_required()
#     def get(self):
#         # users=UsersDB.objects().get(username=)
#         user_id = get_jwt_identity()
#         user = UsersDB.objects.get(id=user_id)
        
#         last_login = user.last_login
#         if last_login is None:
#             return {'gists': 'This is first login. Gists info will appear for future logins.\n '
#                               ' Please logout and login again. '}
       
#         print(user.username)
#         #get all documents with user logged in and document created after last login
#         gists_for_user = UserGists.objects.filter(owner__login=user.username, created_at__gt=last_login)
       
#         return {'message' :'User successfully authenticated.\nGists since last login'+last_login,'gists':gists_for_user.to_json()}
       


# class CreateActivity(Resource):
#     def remove_dots(self,d):
#         new = {}
#         for k, v in d.items():
#             if isinstance(v, dict):
#                 v = self.remove_dots(v)
#             new[k.replace('.', '-')] = v
#         return new   

#     def post(self):
#         """
#         Call this api to update continuously all users' github gists into pipedrive
#         This can be done using a shell script which calls /api/create/activity api.
#         For every user, we get the gists from github and maintain the gists in mongodb.
#         Once put into mongodb, pipedrive api is called to create activity.
#         """
#         users = UsersDB.objects().all()

#         for user in users:
#             gists_response = requests.get("https://api.github.com/users/"+user.username+"/gists")
#             gists_json = json.loads(gists_response.text)
#             for gist in gists_json:
#                 #Mongo doesnt take '$' or '.' in keys , so data has to be cleaned.
#                 gist_cleaned=self.remove_dots(gist)
#                 # UserGists.from_json(json.dumps(gist)).save()
#                 UserGists(**gist_cleaned).save()
#                 #TODO: also convert the gists into pipedrive api activity
#                 #put api_token from pipedrive in query_params
#                 params = {}
#                 #Make POST call to create activity api/v1/activities
#                 activity_payload = {'subject':gist_cleaned, 'type':'task','api_token':user.api_token}
#                 resp = requests.post('https://'+user.company_domain+'.pipedrive.com/api/v1/activities',params=activity_payload)
#                 if resp.status_code == 201:
#                     return resp.text,201
#                 return resp.text, resp.status_code

class TransactionApi(Resource):
    def post(self):
        print(request.form)
        user_id = request.form['user_id']
        print("userif {}".format(user_id))
        ts= request.form.get('ts','')
        txn_amnt=request.form.get('txn_amnt')
        transaction=Transaction(user_id=user_id,
                                # ts=ts,
                                txn_amnt=txn_amnt)
        db.session.add(transaction)
        db.session.commit()
            # flash('Record was successfully added')
        # return jsonify({"message":"User added successfully"})
        return redirect(url_for('transactionapi'))
    
    def get(self):

        response = make_response(render_template('transactions.html',transactions=Transaction.query.all()))
        response.headers['Content-Type'] =  'text/html'
        return response

class IndexPage(Resource):
    def get(self):
        response=make_response(render_template('index.html'))
        response.headers['Content-Type'] =  'text/html'
        return response

class BalanceApi(Resource):
    def get(self):
        # distinct_user_ids = session.query(Transaction.user_id).distinct().all()
        distinct_user_ids=db.session.query(Transaction.user_id).distinct().all()
        print("distinct user ids {}".format(distinct_user_ids))
        for user in distinct_user_ids:
            print("user {}".format(user[0]))
            ret=db.session.query(Transaction).filter(Transaction.user_id==user[0])
            balance=0
            for row in ret:
                print("user_id",row.user_id,"txn_amnt",row.transaction_amt)
                balance+= row.transaction_amt
            print("Balance {}".format(balance))
            balance_obj=Balance(user_id=user[0],balance=balance)
            db.session.add(balance_obj)
            db.session.commit()
                
        response = make_response(render_template('balance.html',balance=Balance.query.all()))
        response.headers['Content-Type'] =  'text/html'
        return response

        # user_id=distinct_user_ids
        # from database.models import transaction_schema
        # result = transaction_schema.dump(distinct_user_ids)
        # print("distinct user ids {}".format(result))
        return jsonify(result)

api.add_resource(IndexPage,'/')
api.add_resource(TransactionApi,'/api/transaction')
api.add_resource(BalanceApi, '/api/balance')


if __name__ == "__main__":
    
    app.run(host='0.0.0.0',port=8000,debug=True)
