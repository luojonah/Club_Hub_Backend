import logging
import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from functools import wraps
from api.jwt_authorize import token_required
from model.event import Event
from __init__ import app
from model.user import User
from api.jwt_authorize import token_required

# Define the blueprint
event_api = Blueprint('event_api', __name__, url_prefix='/api')
api = Api(event_api) # Create an instance of the Api class

class EventAPI: 
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new event.
            """
            current_user = g.current_user # retrieve data of current user
            data = request.get_json() # change json to python dictionary

            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'Event title is required'}, 400
            if 'description' not in data:
                return {'message': 'Event description is required'}, 400
            if 'date' not in data:
                return {'message': 'Event date is required'}, 400

            # Create a new event object
            event = Event(title=data['title'], description=data['description'], date=data['date'])
            event.create()

            return jsonify(event.to_dict())

        def get(self): # display and retrieve all events
            """
            Retrieve all Events.
            """
            events = Event.query.all() # retrieving all events
            if not events:
                return {'message': 'No events found'}, 404  
            return jsonify([event.to_dict() for event in events])  # Return a list of events as JSON
        
        @token_required()
        def put(self):
            """
            Update an event.
            """
            current_user = g.current_user  # Retrieve data of current user
            data = request.get_json()  # Change JSON to Python dictionary

            if not data or 'id' not in data:
                return {'message': 'Event ID is required'}, 400

            event = Event.query.get(data['id'])  # Retrieve event by ID
            if event is None:
                return {'message': 'Event not found'}, 404

            updated_event = event.update(data)
            if updated_event:
                return jsonify(updated_event.to_dict())
            else:
                return {'message': 'An error occurred while updating the event. Please try again.'}, 500

        @token_required()
        def delete(self):
            """
            Delete an event.
            """
            current_user = g.current_user
            data = request.get_json()
            event = Event.query.get(data['id'])
            if event is None:
                return {'message': 'Event not found'}, 404
            event.delete()
            return jsonify({"message": "Event deleted"})

    class _USER(Resource): # user data. only the authenticated user can see the events
        @token_required()
        def get(self):
            """
            Retrieve all events by the current user.
            """
            current_user = g.current_user
            events = Event.query.filter_by(user_id=current_user['uid']).all()
            return jsonify([event.to_dict() for event in events])

    class _BULK_CRUD(Resource): # handle multiple requestet at once
        def post(self):
            """
            Handle bulk event creation by sending POST requests to the single event endpoint.
            """
            events = request.get_json()

            if not isinstance(events, list): # ensure that the input events is a list.
                return {'message': 'Expected a list of event data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client: # This creates a test client for sending HTTP requests to your Flask application
                for event in events:
                    response = client.post('/api/event', json=event) # A POST request is sent to the /api/event endpoint for each event in the events list.

                    if response.status_code == 200: # is checked to determine if the request was successful 
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            return jsonify(results)
        
        def get(self):
            """
            Retrieve all events.
            """
            events = Event.query.all()
            return jsonify([event.to_dict() for event in events])

    """
    Map the _CRUD, _USER, _BULK_CRUD classes to the API endpoints for /event, /event/user, and /events.
    """
    api.add_resource(_CRUD, '/event') 
    api.add_resource(_USER, '/event/user')
    api.add_resource(_BULK_CRUD, '/events')