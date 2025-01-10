from flask import Blueprint, request, jsonify
from model.event import Event
from __init__ import db


event_api = Blueprint('event_api', __name__, url_prefix='/api/event')


STATIC_EVENT_DATA = {
    "title": "Math",
    "description": "Math Olympiad",
    "date": "2025-02-01"
}


@event_api.route('', methods=['POST'])
def create_event():
    """
    Endpoint to create a new event.
    """
    data = request.get_json()


   


    # Validate the input
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')


    if not title or not description or not date:
        return jsonify({"error": "Missing required fields"}), 400


    # Create a new event
    new_event = Event(title=title, description=description, date=date)
    db.session.add(new_event)
    db.session.commit()


    return jsonify(new_event.to_dict()), 201


@event_api.route('', methods=['GET'])
def get_events():
    """
    Endpoint to fetch all events.
    """
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200