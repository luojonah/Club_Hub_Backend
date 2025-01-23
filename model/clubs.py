from flask import Blueprint, jsonify
from flask_restful import Api, Resource  # used for REST API building
from club import Club  # Import the Club model

club1_api = Blueprint('club1_api', __name__, url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(club1_api)

class Club1API:
    class _Clubs(Resource):
        def get(self):
            """
            Retrieves all clubs from the database.
            """
            clubs = Club.query.all()  # Fetch all clubs
            club_list = [club.to_dict() for club in clubs]  # Convert each club to a dictionary
            return jsonify(club_list)

    class _Gemini(Resource):
        def get(self):
            """
            Placeholder for Gemini endpoint.
            """
            return jsonify({"message": "This endpoint is under construction."})

    # Building REST API endpoints
    api.add_resource(_Clubs, '/club1/clubs')
    api.add_resource(_Gemini, '/club1/gemini')
