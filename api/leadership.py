from flask import Blueprint, request, jsonify
# from flask_restful import API, Resource
from model.leadership import Leadership
from __init__ import db



# Creating blueprint for the leadership API
leadership_api = Blueprint('leadership_api', __name__, url_prefix='/api/leadership')
# api = API(leadership_api)

# class LeadershipAPI(Resource);

# POST method to create a new leadership record

@leadership_api.route('', methods=['POST'])
def create_leadership():
    """
    Endpoint to create a new leadership application.
    """
    data = request.get_json()

    # Validating input and defining variables
    name = data.get('name')
    role = data.get('role')
    club = data.get('club')
    experience = data.get('experience')

    # All information must be filled out
    if not name or not role or not club or not experience:
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new leadership application
    new_leadership = Leadership(name=name, role=role, club=club, experience=experience)
    created_leadership = new_leadership.create()

    # Ensure no duplicates
    if created_leadership:
        return jsonify(created_leadership.to_dict()), 201
    else:
        return jsonify({"error": "Failed to create leadership application. Name might already exist."}), 400


# GET method to retrieve all leadership applications
@leadership_api.route('', methods=['GET'])
def get_leaderships():
    """
    Endpoint to fetch all leadership applications.
    """
    leaderships = Leadership.query.all()
    return jsonify([leadership.to_dict() for leadership in leaderships]), 200

# DELETE method to delete a specific leadership application
@leadership_api.route('/<int:id>', methods=['DELETE'])
def delete_leadership(id):
    """
    Endpoint to delete a leadership application by ID.
    """
    leadership = Leadership.query.get(id)
    if not leadership:
        return jsonify({"error": "Leadership application not found"}), 404  # Return error if not found

    db.session.delete(leadership)  # Delete the leadership record from the database
    db.session.commit()  # Commit the transaction
    return jsonify({"message": "Leadership application deleted successfully"}), 200


# PUT method to update a specific leadership application
@leadership_api.route('/<int:id>', methods=['PUT'])
def update_leadership(id):
    """
    Endpoint to update a leadership application by ID.
    """
    data = request.get_json()

    leadership = Leadership.query.get(id)
    if not leadership:
        return jsonify({"error": "Leadership application not found"}), 404

    # Update fields if they are provided in the request
    name = data.get('name')
    role = data.get('role')
    club = data.get('club')
    experience = data.get('experience')

    if name:
        leadership.name = name
    if role:
        leadership.role = role
    if club:
        leadership.club = club
    if experience:
        leadership.experience = experience

    try:
        db.session.commit()
        return jsonify(leadership.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update leadership application: {str(e)}"}), 500


