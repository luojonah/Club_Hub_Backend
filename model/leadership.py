from __init__ import db, app
from sqlalchemy.exc import IntegrityError
import logging
import requests
from flask import jsonify, request

# Creating a container for leadership application information
class Leadership(db.Model):
    """
    Leadership Model
    Represents a leadership application with details such as name, role, club, and experience.
    """
    __tablename__ = 'leaderships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    club = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.String(255), nullable=False)

    def __init__(self, name, role, club, experience):
        self.name = name
        self.role = role
        self.club = club
        self.experience = experience

    # Save the current Leadership instance to the database.
    def create(self):
        """
        Creates a new leadership application in the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError: Could not create leadership '{self.name}'. Error: {str(e)}")
            return None
        
    # Updates the current object’s attributes with new data.
    def update(self, data):
        """
        Updates the Leadership instance with the provided data.
        """
        for key, value in data.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError: Could not update leadership '{self.name}'. Error: {str(e)}")
            
    # Converts the Leadership object into a dictionary with all its attributes.
    def to_dict(self):
        """
        Converts the Leadership object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "club": self.club,
            "experience": self.experience
        }

    # Similar to to_dict, this method returns a dictionary representation.
    def read(self):
        """
        Converts the Leadership object to a dictionary with specific fields.
        """
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "club": self.club,
            "experience": self.experience
        }

    # Updates or creates Leadership records from a list of dictionaries.
    @staticmethod
    def restore(data):
        """
        Restores leadership data from a given dataset.
        
        Args:
            data (list): A list of dictionaries containing leadership data.
        """
        for leadership_data in data:
            # Remove 'id' if it exists in the data
            leadership_data.pop('id', None)
            
            name = leadership_data.get("name")
            if not name:
                logging.warning("Missing name in leadership data, skipping entry.")
                continue

            # Check if the leadership entry exists
            leadership = Leadership.query.filter_by(name=name).first()
            if leadership:
                # Update the existing entry
                for key, value in leadership_data.items():
                    setattr(leadership, key, value)
                db.session.commit()
                logging.info(f"Updated leadership entry: {name}")
            else:
                # Create a new entry
                leadership = Leadership(**leadership_data)
                db.session.add(leadership)
                db.session.commit()
                logging.info(f"Created new leadership entry: {name}")
                
    @staticmethod
    def fetch_clubs():
        """
        Fetches club data from the external API and updates or creates new club entries.
        """
        api_url = 'http://127.0.0.1:8887/api/clubs'  # Your API endpoint

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                clubs = response.json()

                # Assuming 'clubs' is a list of dictionaries
                for club in clubs:
                    club_name = club.get('name')
                    if not club_name:
                        logging.warning("Club data missing 'name', skipping entry.")
                        continue

                    # Check if the club already exists in the database
                    existing_club = Leadership.query.filter_by(club=club_name).first()
                    if existing_club:
                        logging.info(f"Club '{club_name}' already exists in the database.")
                    else:
                        # Create a new leadership entry for the club if it doesn't exist
                        leadership = Leadership(name='Default Name', role='Default Role', club=club_name, experience='No experience')
                        db.session.add(leadership)
                        db.session.commit()
                        logging.info(f"Created new leadership entry for club '{club_name}'.")
            else:
                logging.error(f"Failed to fetch clubs from API. Status code: {response.status_code}")
                error = response.json()
                logging.error(f"Error message: {error.get('message')}")
        except Exception as e:
            logging.error(f"Error occurred while fetching club data: {str(e)}")

    def delete(self):
        """
        Deletes the Leadership instance from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            logging.info(f"Deleted leadership entry: {self.name}")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting leadership '{self.name}': {str(e)}")

# API endpoint to fetch leadership applications
@app.route('/api/leadership', methods=['GET'])
def get_applications():
    """
    Fetches leadership applications from the database with pagination.
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        # Query the database for leadership applications
        applications = Leadership.query.paginate(page=page, per_page=limit)

        # Create the response structure
        response = {
            "applications": [app.to_dict() for app in applications.items],
            "totalCount": applications.total
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error fetching applications: {str(e)}")
        return jsonify({"error": "Error fetching applications"}), 500

# Initialization function for Leadership table
def initLeadership():
    """
    Initializes the Leadership table and adds some test data.
    """
    with app.app_context():
        # Create database and tables
        db.create_all()
        # Tester data for table
        leaderships = [
            Leadership(name='John Doe', role='President', club='AI Club', experience='2 years of leadership in tech clubs'),
            Leadership(name='Jane Smith', role='Secretary', club='Photography Club', experience='1 year of experience in administration')
        ]
        
        for leadership in leaderships:
            try:
                leadership.create()
                print(f"Leadership created: {repr(leadership)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate leadership entry: {leadership.name}")
