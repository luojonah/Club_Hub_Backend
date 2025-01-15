from flask import Blueprint, request, jsonify
from model.event import Event


# Define the blueprint
event_api = Blueprint('event_api', __name__, url_prefix='/api/event')


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


    # Create a new event using the model method
    new_event = Event.create(title=title, description=description, date=date)


    return jsonify(new_event.to_dict()), 201


@event_api.route('', methods=['GET'])
def get_events():
    """
    Endpoint to fetch all events.
    """
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200


@event_api.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """
    Endpoint to delete an event by ID.
    """
    if Event.delete(event_id):
        return jsonify({"message": "Event deleted"}), 200
    else:
        return jsonify({"error": "Event not found"}), 404