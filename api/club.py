import logging
import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from __init__ import app
from functools import wraps
from model.club import Club

import jwt
from model.user import User

# define bluepring and api endpoint
club_api = Blueprint('club_api', __name__, url_prefix='/api')
api = Api(club_api)

def token_required(func_to_guard):
        @wraps(func_to_guard)
        def decorated(*args, **kwargs):
            token = request.cookies.get(current_app.config["JWT_TOKEN_NAME"])

            if not token:
                return {
                    "message": "Token is missing",
                    "error": "Unauthorized"
                }, 401

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.filter_by(_uid=data["_uid"]).first()
                if not current_user:
                    return {
                        "message": "User not found",
                        "error": "Unauthorized",
                        "data": data
                    }, 401
                    
                # Authentication succes, set the current_user in the global context (Flask's g object)
                g.current_user = current_user
            except jwt.ExpiredSignatureError:
                return {
                    "message": "Token has expired",
                    "error": "Unauthorized"
                }, 401
            except jwt.InvalidTokenError:
                return {
                    "message": "Invalid token",
                    "error": "Unauthorized"
                }, 401
            except Exception as e:
                return {
                    "message": "An error occurred",
                    "error": str(e)
                }, 500

            # Call back to the guarded function if all checks pass
            return func_to_guard(*args, **kwargs)
        return decorated

# creates class for api (CRUD endpoints)
class ClubAPI:
    class _CRUD(Resource):
        # post all clubs
        @token_required
        def post(self):
            """
            Create a new club.
            """
            current_user = g.current_user
            data = request.get_json()

            # make sure all data is filled out (null=False)
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data:
                return {'message': 'Club name is required'}, 400
            if 'description' not in data:
                return {'message': 'Club description is required'}, 400
            if 'topics' not in data:
                return {'message': 'Club topics are required'}, 400

            # Create a new club object
            club = Club(name=data['name'], description=data['description'], topics=data['topics'])
            club.create()
            # return club as JSON
            return jsonify(club.to_dict())

        # get all clubs
        @token_required
        def get(self):
            """
            Retrieve all clubs.
            """
            clubs = Club.query.all()  # Get all clubs from the database
            if not clubs:
                return {'message': 'No clubs found'}, 404  # If no clubs exist
            return jsonify([club.to_dict() for club in clubs])  # Return a list of clubs as JSON

        # update club information
        @token_required
        def put(self):
            """
            Update a club.
            """
            current_user = g.current_user
            data = request.get_json()

            # Find the club by ID
            club = Club.query.get(data['id'])
            if club is None:
                return {'message': 'Club not found'}, 404

            # Update the club with the provided data
            club.name = data['name']
            club.description = data['description']
            club.topics = data['topics']

            # Pass the data to the update method
            club.update(data)  # Pass the data dictionary here

            return jsonify(club.to_dict())

        # delete a club
        @token_required
        def delete(self):
            """
            Delete a club.
            """
            current_user = g.current_user
            data = request.get_json()
            club = Club.query.get(data['id'])
            if club is None:
                return {'message': 'Club not found'}, 404
            club.delete()
            return jsonify({"message": "Club deleted"})

    class _USER(Resource):
        @token_required
        def get(self):
            """
            Retrieve all clubs by the current user.
            """
            current_user = g.current_user
            clubs = Club.query.filter_by(user_id=current_user.id).all()
            return jsonify([club.to_dict() for club in clubs])

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Handle bulk club creation by sending POST requests to the single club endpoint.
            """
            clubs = request.get_json()

            if not isinstance(clubs, list):
                return {'message': 'Expected a list of club data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for club in clubs:
                    response = client.post('/api/club', json=club)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            return jsonify(results)
        
        def get(self):
            """
            Retrieve all clubs.
            """
            clubs = Club.query.all()
            return jsonify([club.to_dict() for club in clubs])

    """
    Map the _CRUD, _USER, _BULK_CRUD classes to the API endpoints for /club, /club/user, /clubs, and /clubs/filter.
    """
    api.add_resource(_CRUD, '/club')
    api.add_resource(_USER, '/club/user')
    api.add_resource(_BULK_CRUD, '/clubs')