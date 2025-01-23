from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from functools import wraps
from model.interest import Interest  # Import Interest model
from api.jwt_authorize import token_required  # Import the legit token_required decorator
from __init__ import db  # Use the existing SQLAlchemy instance

# Blueprint setup
interest_api = Blueprint('interest_api', __name__, url_prefix='/api')
api = Api(interest_api)

class InterestsAPI(Resource):
    @token_required
    def post(self):
        """
        Save user interests (clear and replace with new ones).
        """
        current_user = g.current_user['uid']
        data = request.get_json()

        if not data or 'interests' not in data:
            return {"message": "No interests provided"}, 400

        interests = data['interests']
        if not isinstance(interests, list):
            return {"message": "Interests must be a list"}, 400

        # Clear existing interests
        Interest.query.filter_by(user_id=current_user).delete()

        # Add new interests
        for interest in interests:
            new_interest = Interest(user_id=current_user, interest=interest)
            new_interest.create()

        return {"message": "Interests saved successfully"}, 200

    @token_required
    def get(self):
        """
        Retrieve saved interests for the current user.
        """
        current_user = g.current_user['uid']
        interests = Interest.query.filter_by(user_id=current_user).all()
        return {"interests": [i.read() for i in interests]}, 200

    @token_required
    def put(self):
        """
        Update specific user interest(s).
        """
        current_user = g.current_user['uid']
        data = request.get_json()

        if not data or 'interests' not in data:
            return {"message": "No interests provided"}, 400

        interests = data['interests']
        if not isinstance(interests, list):
            return {"message": "Interests must be a list"}, 400

        for interest_data in interests:
            old_interest = interest_data.get("old")
            new_interest = interest_data.get("new")
            if not old_interest or not new_interest:
                return {"message": "Both old and new interests must be provided"}, 400

            existing_interest = Interest.query.filter_by(user_id=current_user, interest=old_interest).first()
            if existing_interest:
                existing_interest.update(new_interest)

        return {"message": "Interests updated successfully"}, 200

    @token_required
    def delete(self):
        """
        Delete specific user interest(s).
        """
        current_user = g.current_user['uid']
        data = request.get_json()

        if not data or 'interests' not in data:
            return {"message": "No interests provided"}, 400

        interests = data['interests']
        if not isinstance(interests, list):
            return {"message": "Interests must be a list"}, 400

        for interest in interests:
            existing_interest = Interest.query.filter_by(user_id=current_user, interest=interest).first()
            if existing_interest:
                existing_interest.delete()

        return {"message": "Interests deleted successfully"}, 200

# Register the resource to the API
api.add_resource(InterestsAPI, '/interests')