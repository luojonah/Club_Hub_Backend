# club.py
from flask import Blueprint, request, jsonify
from model.club import Club
from __init__ import db

club_api = Blueprint('club_api', __name__, url_prefix='/api/club')

@club_api.route('', methods=['POST'])
def create_club():
    """
    Endpoint to create a new club.
    """
    data = request.get_json()

    # Validate the input
    name = data.get('name')
    description = data.get('description')
    topics = data.get('topics')

    if not name or not description or not topics:
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new club
    new_club = Club(name=name, description=description, topics=topics)
    created_club = new_club.create()

    if created_club:
        return jsonify(created_club.to_dict()), 201
    else:
        return jsonify({"error": "Failed to create club. Club name might already exist."}), 400

@club_api.route('', methods=['GET'])
def get_clubs():
    """
    Endpoint to fetch all clubs.
    """
    clubs = Club.query.all()
    return jsonify([club.to_dict() for club in clubs]), 200

