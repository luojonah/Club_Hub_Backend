from __init__ import db, app
from sqlalchemy.exc import IntegrityError
import logging
from model.gemini import Gemini
from __init__ import db 
from api.gemini import gemini_api


class Gemini(db.Model):
    """
    Gemini Model
    Represents an AI-generated response to a user's question.
    """
    __tablename__ = 'gemini'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    question = db.Column(db.Text, nullable=False)  # User's question
    response = db.Column(db.Text, nullable=False)  # AI's response
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp of the entry

    def __init__(self, question, response):
        self.question = question
        self.response = response

    def create(self):
        """
        Saves the Gemini object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError: Could not save response for question '{self.question}'. Error: {str(e)}")
            return None

    def to_dict(self):
        """
        Converts the Gemini object to a dictionary.
        """
        return {
            "id": self.id,
            "question": self.question,
            "response": self.response,
            "timestamp": self.timestamp
        }

# Initialization function for the Gemini table
def initGemini():
    """
    Creates the Gemini table and adds sample data.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        print("Gemini table initialized.")
