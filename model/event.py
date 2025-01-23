import logging
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Event(db.Model): # define the columns of the table, This class inherits from the db.Model class, which is a base class for all models in Flask-SQLAlchemy.
    """
    Event Model
    
    Represents an event with a title, description, and date.
    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, title, description, date): #  It sets up the initial state of the object with the given arguments.
        self.title = title # every instance of the class will have a title and description associated with it.
        self.description = description
        if isinstance(date, str): #  This checks if the date parameter is a string.
            self.date = datetime.strptime(date, '%Y-%m-%d').date() # Parses the string into a datetime object
        else:
            self.date = date

    def __repr__(self): # This method returns a string representation of the object.
        return f"<Event(id={self.id}, title={self.title}, description={self.description}, date={self.date})>"

    def to_dict(self):
        """
        Convert the Event object into a dictionary format.
        This method is used to return the event object as JSON in API responses.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.strftime('%Y-%m-%d')
        }
        
    def read(self): # returns the result of calling the to_dict(), access an object's data 
        return self.to_dict()

    def create(self):
        """
        Creates a new event in the database.
        """
        try:
            db.session.add(self) #  object (self) and add it to the session
            db.session.commit() # save changes to db
        except IntegrityError as e:
            db.session.rollback() # undoes the transaction
            logging.warning(f"IntegrityError: Could not create event '{self.title}' due to {str(e)}.")
            return None
        return self

    def update(self, data):
        """
        Updates the event with new data.
        """
        for key, value in data.items():
            if hasattr(self, key):
                # Convert date string to date object if necessary
                if key == 'date' and isinstance(value, str):
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(self, key, value)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update event '{self.title}' due to {str(e)}.")
            return None
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"Could not delete event '{self.title}' due to IntegrityError.")
            return None

    @staticmethod # This decorator is used to define a method that does not operate on an instance of the class.
    def restore(data): #  Trestore the database with the data provided.
        for event_data in data: # iterates over the data provided.
            _ = event_data.pop('id', None) # removes id
            event = Event.query.filter_by(title=event_data['title']).first() # retrieves the event by title
            if event:
                event.update(event_data)
            else:
                event = Event(**event_data)
                event.create()

def initEvents(): # initEvents` function initializes the Events table with test data.
    """
    Initializes the Events table with test data.
    """
    with app.app_context(): # creates an application context for the app.
        db.create_all() 
        events = [ # creates a list of Event objects
            Event(title='Tech Conference', description='A conference about the latest in technology.', date='2025-05-20'),
            Event(title='Music Festival', description='A festival featuring various music artists.', date='2025-06-15'),
            Event(title='Art Expo', description='An expo showcasing modern art.', date='2025-07-10'),
        ]
        for event in events: 
            try:
                event.create()
                print(f"Record created: {repr(event)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Records exist or duplicate error: {event.title}, {str(e)}")