from flask import Flask, request
from flask_restful import Resource, Api,reqparse,request
import json
import datetime
from flask.json import jsonify
from flask_mongoengine import MongoEngine
from database.db_config import initialize_db
from database.models import UsersDB,UserGists
import  datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import json

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
jwt = JWTManager(app)
app.config['MONGODB_SETTINGS'] = {
    
       'db': 'test_db',
        'host': 'mongodb+srv://cluster0.hpqql.mongodb.net',
        'port': 27017,
        'username':'mongo_user2',
        'password':'Cisco123'
    }

initialize_db(app)
#flask-restful framework
api = Api(app)

class SignupApi(Resource):
     def post(self):
        body = request.get_json()
        user = UsersDB(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 201

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = UsersDB.objects.get(username=body.get('username'))
        authorized = user.check_password(body.get('password'))

        

        if not authorized:
            return {'message': 'Email or password invalid'}, 401
        else:
            last_login = user['last_login']
            user.update_time()
            user.save()
            expires = datetime.timedelta(minutes=10)
            access_token = create_access_token(identity = str(user.id), 
                                            expires_delta = expires)
    
            return {'message': 'User successfully authenticated',
                    "last_login": str(last_login),
                    'token': access_token
                     },201
        

    
class LatestGists(Resource):
    #cannot run background task for specific user , update for all users in database
    @jwt_required()
    def get(self):
        # users=UsersDB.objects().get(username=)
        user_id = get_jwt_identity()
        user = UsersDB.objects.get(id=user_id)
        
        last_login = user.last_login
        if last_login is None:
            return {'gists': 'This is first login. Gists info will appear for future logins.\n '
                              ' Please logout and login again. '}
        # for user in users:
        #     print("getting gist for user {}".format(user.username))
        gists_response = requests.get("https://api.github.com/users/"+user.username+"/gists")
        gists_json = json.loads(gists_response.text)
        if user.username == 'gitwithash':
            return { 'gists':gists_json}
        #code to filter documents after last_login
        objects_since_llogin = UsersDB.objects.filter(created_at__gt=last_login)
        return {'message' :'Gists since last login'+last_login,'gists':objects_since_llogin}
        #     # UserGists(gists_json).save()


class CreateActivity(Resource):
    def remove_dots(self,d):
        new = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.remove_dots(v)
            new[k.replace('.', '-')] = v
        return new   

    def post(self):
        """
        Call this api to update continuously all users' github gists into pipedrive
        This can be done using a shell script which calls /api/create/activity api.
        For every user, we get the gists from github and maintain the gists in mongodb.
        Once put into mongodb, pipedrive api is called to create activity.
        """
        users = UsersDB.objects().all()

        for user in users:
            gists_response = requests.get("https://api.github.com/users/"+user.username+"/gists")
            gists_json = json.loads(gists_response.text)
            for gist in gists_json:
                #Mongo doesnt take '$' or '.' in keys , so data has to be cleaned.
                gist_cleaned=self.remove_dots(gist)
                # UserGists.from_json(json.dumps(gist)).save()
                UserGists(**gist_cleaned).save()
                #TODO: also convert the gists into pipedrive api activity



api.add_resource(SignupApi, '/api/signup')
api.add_resource(LoginApi, '/api/login')
api.add_resource(LatestGists, '/api/create/activity')
api.add_resource(CreateActivity, '/api/create/gists')


if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)
