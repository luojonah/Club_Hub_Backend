# club.py
import logging
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from __init__ import db


class Club(db.Model):
    """
    Club Model
    
    Represents a club entity within the application.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the club.
        name (db.Column): A string representing the name of the club.
        description (db.Column): A string representing the description of the club.
        topics (db.Column): A JSON blob representing the topics associated with the club.
    """
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    topics = db.Column(JSON, nullable=False)

    def __init__(self, name, description, topics):
        """
        Constructor for Club.

        Args:
            name (str): Name of the club.
            description (str): Description of the club.
            topics (list or dict): Topics associated with the club.
        """
        self.name = name
        self.description = description
        self.topics = topics

    def __repr__(self):
        """
        String representation of the Club object.
        
        Returns:
            str: A string representation of the club object.
        """
        return f"Club(id={self.id}, name={self.name}, description={self.description}, topics={self.topics})"

    def create(self):
        """
        Save the club to the database.
        
        Returns:
            Club: The created club object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create club '{self.name}' due to {str(e)}.")
            return None
        return self

    def read(self):
        """
        Retrieve the club data as a dictionary.
        
        Returns:
            dict: A dictionary containing the club data.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topics": self.topics
        }

    def update(self, data):
        """
        Update the club with new data.
        
        Args:
            data (dict): A dictionary containing updated club information.
        
        Returns:
            Club: The updated club object, or None on error.
        """
        self.name = data.get('name', self.name)
        self.description = data.get('description', self.description)
        self.topics = data.get('topics', self.topics)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update club '{self.name}' due to {str(e)}.")
            return None
        return self

    def delete(self):
        """
        Delete the club from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
