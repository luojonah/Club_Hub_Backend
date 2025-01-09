from flask import Blueprint, jsonify
from flask_restful import Api, Resource # used for REST API building

club1_api = Blueprint('club1_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(club1_api)

class Club1API:        
    class _Clubs(Resource): 
        def get(self):
            gemini_data = {
                "ClubName": "Tech Innovators",
                "President": "Alex Johnson",
                "MembersCount": 40,
                "Email": "techinnovators@gmail.com",
                "Location": "San Diego"
            }
            return jsonify(gemini_data)
    
    class _Gemini(Resource): 
        def get(self):
           # implement the get method 
           pass

    # building RESTapi endpoint
    api.add_resource(_Clubs, '/club1/clubs')          
    api.add_resource(_Gemini, '/club1/gemini')