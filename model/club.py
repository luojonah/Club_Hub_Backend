# club.py
from __init__ import db, app
from sqlalchemy.exc import IntegrityError
import logging

class Club(db.Model):
    """
    Club Model
    Represents a club with its name, description, and topics.
    """
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    topics = db.Column(db.JSON, nullable=False)

    def __init__(self, name, description, topics):
        self.name = name
        self.description = description
        self.topics = topics

    def create(self):
        """
        Creates a new club in the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError: Could not create club '{self.name}'. Error: {str(e)}")
            return None

    def to_dict(self):
        """
        Converts the Club object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topics": self.topics
        }


def initClubs():
    """
    The initClubs function creates the Club table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Club objects with test data.
    
    Raises:
        IntegrityError: An error occurred when adding the test data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        clubs = [
            Club(name='AI Club', description='A club focused on artificial intelligence and machine learning.', topics=['AI', 'ML', 'Robots']),
            Club(name='Photography Club', description='A club for enthusiasts of photography and visual storytelling.', topics=['Photos', 'Arts']),
            Club(name='Cybersecurity Club', description='A club dedicated to learning and practicing cybersecurity.', topics=['Cyber', 'Code', 'Chain']),
        ]
        
        for club in clubs:
            try:
                club.create()
                print(f"Record created: {repr(club)}")
            except IntegrityError:
                '''Fails with bad or duplicate data'''
                db.session.rollback()
                print(f"Records exist or duplicate error: {club.name}")
