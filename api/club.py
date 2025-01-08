# club_api.py
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.club import Club

club_api = Blueprint('club_api', __name__, url_prefix='/api')
api = Api(club_api)

class ClubAPI:
    """
    API endpoints for the Club model.
    """

    class _CRUD(Resource):
        # @token_required()
        def post(self):
            """
            Create a new club.
            """
            data = request.get_json()

            # Validate input data
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data:
                return {'message': 'Club name is required'}, 400
            if 'description' not in data:
                return {'message': 'Club description is required'}, 400
            if 'topics' not in data:
                data['topics'] = []

            # Create a new club
            club = Club(data['name'], data['description'], data['topics'])
            created_club = club.create()
            if not created_club:
                return {'message': 'Club could not be created, check input or database constraints'}, 400

            return jsonify(created_club.read())

        def get(self):
            """
            Retrieve all clubs or a single club by ID.
            """
            data = request.args

            if 'id' in data:
                club = Club.query.get(data['id'])
                if club is None:
                    return {'message': 'Club not found'}, 404
                return jsonify(club.read())

            # Retrieve all clubs
            clubs = Club.query.all()
            json_ready = [club.read() for club in clubs]
            return jsonify(json_ready)

        # @token_required()
        def put(self):
            """
            Update a club.
            """
            data = request.get_json()

            # Validate club ID
            if 'id' not in data:
                return {'message': 'Club ID is required'}, 400

            # Find the club
            club = Club.query.get(data['id'])
            if club is None:
                return {'message': 'Club not found'}, 404

            # Update the club
            updated_club = club.update(data)
            if not updated_club:
                return {'message': 'Club could not be updated'}, 400

            return jsonify(updated_club.read())

        # @token_required()
        def delete(self):
            """
            Delete a club.
            """
            data = request.get_json()

            # Validate club ID
            if 'id' not in data:
                return {'message': 'Club ID is required'}, 400

            # Find the club
            club = Club.query.get(data['id'])
            if club is None:
                return {'message': 'Club not found'}, 404

            # Delete the club
            club.delete()
            return {'message': 'Club deleted successfully'}

    api.add_resource(_CRUD, '/club')

