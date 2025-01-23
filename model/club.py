import logging
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User

class Club(db.Model):
    # names the table clubs in database
    __tablename__ = 'clubs'

    # defines columns in database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    topics = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users._uid'), nullable=False)

    # initializes the club object
    def __init__(self, name, description, topics, user_id=None):
        self.name = name
        self.description = description
        self.topics = topics
        self.user_id = user_id if user_id is not None else "luojonah"

    # returns a string representation of the club object
    def __repr__(self):
        return f"<Club(id={self.id}, name={self.name}, description={self.description})>"

    # converts all club information into dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topics": self.topics,
            "user_id": self.user_id
        }

    # creates a new club in the database
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create club '{self.name}' due to {str(e)}.")
            return None
        return self

    # reads club data from database and returns as dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topics": self.topics,
            "user_id": self.user_id
        }

    # updates club data in database
    def update(self, club_data):
        """
        Updates the club with new data.
        """
        try:
            for key, value in club_data.items():
                setattr(self, key, value)  # Dynamically update attributes of the club

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update club '{self.name}' due to {str(e)}.")
            return None
        return self

    # delete club from database
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"Could not delete club '{self.name}' due to IntegrityError.")
            return None

    @staticmethod
    def restore(data):
        for club_data in data:
            _ = club_data.pop('id', None)  # Remove 'id' from club_data
            name = club_data.get("name", None)
            club = Club.query.filter_by(name=name).first()
            if club:
                club.update(club_data)  # Pass club_data to update
            else:
                club = Club(**club_data)
                club.create()


# initializes the clubs table with test data
def initClubs():
    with app.app_context():
        # create the table
        db.create_all()
        # tester data
        clubs = [
            Club(name='AI Club', description='A club focused on artificial intelligence and machine learning.', topics=['AI', 'ML', 'Robots'], user_id='Charlie Brown'),
            Club(name='Photography Club', description='A club for enthusiasts of photography and visual storytelling.', topics=['Photos', 'Arts'], user_id='Snoopy'),
            Club(name='Cybersecurity Club', description='A club dedicated to learning and practicing cybersecurity.', topics=['Cyber', 'Code', 'Chain'], user_id='mommybobby135'),
        ]
        for club in clubs:
            try:
                club.create()
                print(f"Record created: {repr(club)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Records exist or duplicate error: {club.name}")

