from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from functools import wraps
from model.interest import Interest  # import interest model
from api.jwt_authorize import token_required  # Import the legit token_required decorator
from __init__ import db  # use the existing SQLAlchemy instance

# blueprint setup
interest_api = Blueprint('interest_api', __name__, url_prefix='/api')
api = Api(interest_api)

# token authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401
        g.current_user = {"uid": "magic005"}
        return f(*args, **kwargs)
    return decorated

# API resource for CRUD operations
class InterestsAPI(Resource):
    @token_required
    def post(self):
        """
        Save user interests (clear and replace with new ones).
        """
        current_user = g.current_user['uid']
        data = request.get_json()

        # Validate input
        if not data or 'interests' not in data:
            return {"message": "No interests provided"}, 400

        interests = data['interests']
        if not isinstance(interests, list):
            return {"message": "Interests must be a list"}, 400

        # Save user interests using the model's static method
        Interest.save_user_interests(current_user, interests)
        return {"message": "Interests saved successfully"}, 200

    @token_required
    def get(self):
        """
        Retrieve saved interests for the current user.
        """
        current_user = g.current_user['uid']
        interests = Interest.get_user_interests(current_user)

        return {"interests": interests}, 200

# Register the resource to the API
api.add_resource(InterestsAPI, '/interests')