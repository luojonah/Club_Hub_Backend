import logging
from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class Club(db.Model):
    """
    Club Model
    
    Represents a club with its name, description, topics, and a user who created it.
    """
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    topics = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, description, topics, user_id=None):
        self.name = name
        self.description = description
        self.topics = topics
        self.user_id = user_id if user_id is not None else 1

    def __repr__(self):
        return f"<Club(id={self.id}, name={self.name}, description={self.description})>"

    def to_dict(self):
        """
        Convert the Club object into a dictionary format.
        This method is used to return the club object as JSON in API responses.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topics": self.topics,
            "user_id": self.user_id
        }

    def create(self):
        """
        Creates a new club in the database.
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
        Retrieves the club data and returns it as a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topics": self.topics,
            "user_id": self.user_id
        }

    def update(self):
        """
        Updates the club with new data.
        """
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update club '{self.name}' due to {str(e)}.")
            return None
        return self

    def delete(self):
        """
        Deletes the club from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"Could not delete club '{self.name}' due to IntegrityError.")
            return None

    @staticmethod
    def restore(data):
        """
        Restores club data from provided list, creating or updating clubs.
        """
        for club_data in data:
            _ = club_data.pop('id', None)  # Remove 'id' if it exists
            club = Club.query.filter_by(name=club_data['name']).first()
            if club:
                club.update(club_data)
            else:
                club = Club(**club_data)
                club.create()

def initClubs():
    """
    Initializes the Clubs table with test data.
    """
    with app.app_context():
        db.create_all()
        clubs = [
            Club(name='AI Club', description='A club focused on artificial intelligence and machine learning.', topics=['AI', 'ML', 'Robots'], user_id=1),
            Club(name='Photography Club', description='A club for enthusiasts of photography and visual storytelling.', topics=['Photos', 'Arts'], user_id=2),
            Club(name='Cybersecurity Club', description='A club dedicated to learning and practicing cybersecurity.', topics=['Cyber', 'Code', 'Chain'], user_id=1),
        ]
        for club in clubs:
            try:
                club.create()
                print(f"Record created: {repr(club)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Records exist or duplicate error: {club.name}")

