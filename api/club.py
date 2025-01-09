# club.py
from flask import Blueprint, request, jsonify
from model.club import Club
from __init__ import db

# creating blueprint for the club api 
club_api = Blueprint('club_api', __name__, url_prefix='/api/club')

# POST method which sends inputted data from frontend into schema table
@club_api.route('', methods=['POST'])
def create_club():
    """
    Endpoint to create a new club.
    """
    data = request.get_json()

    # validating input and defining variables to input values
    name = data.get('name')
    description = data.get('description')
    topics = data.get('topics')

    # all information must be filled out (null= True)
    if not name or not description or not topics:
        return jsonify({"error": "Missing required fields"}), 400

    # create a new club
    new_club = Club(name=name, description=description, topics=topics)
    created_club = new_club.create()

    # making sure there's not repeat in clubs
    if created_club:
        return jsonify(created_club.to_dict()), 201
    else:
        return jsonify({"error": "Failed to create club. Club name might already exist."}), 400


# retrieving club information from clubs database schema table
@club_api.route('', methods=['GET'])
def get_clubs():
    """
    Endpoint to fetch all clubs.
    """
    clubs = Club.query.all()
    return jsonify([club.to_dict() for club in clubs]), 200

