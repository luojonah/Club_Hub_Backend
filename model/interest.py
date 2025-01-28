from __init__ import app, db
import logging
from sqlalchemy.exc import IntegrityError

class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    interest = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, interest):
        self.user_id = user_id
        self.interest = interest

    @staticmethod
    def get_user_interests(user_id):
        return [interest.interest for interest in Interest.query.filter_by(user_id=user_id).all()]

    @staticmethod
    def save_user_interests(user_id, interests):
        # clear existing interests (straight up del)
        Interest.query.filter_by(user_id=user_id).delete()
        # add new interests
        for interest in interests:
            db.session.add(Interest(user_id, interest))
        db.session.commit()

    # Restore stuff thing
    @staticmethod
    def restore(data):
        """
        Restores interest data from a given dataset.
        
        Args:
            data (list): A list of dictionaries containing interest data.
        """
        for interest_data in data:
            interest_id = interest_data.pop('id', None)  # Remove 'id' from data if it exists
            user_id = interest_data.get("user_id")
            interest_name = interest_data.get("interest")
            
            if not user_id or not interest_name:
                logging.warning("Missing user_id or interest in data, skipping entry.")
                continue

            # Check if the interest already exists for the user
            existing_interest = Interest.query.filter_by(user_id=user_id, interest=interest_name).first()
            if existing_interest:
                # Update the existing interest (if additional fields are added in the future)
                for key, value in interest_data.items():
                    setattr(existing_interest, key, value)
                db.session.commit()
                logging.info(f"Updated interest entry: {interest_name} for user_id: {user_id}")
            else:
                # Create a new interest entry
                try:
                    new_interest = Interest(user_id=user_id, interest=interest_name)
                    db.session.add(new_interest)
                    db.session.commit()
                    logging.info(f"Created new interest entry: {interest_name} for user_id: {user_id}")
                except IntegrityError as e:
                    db.session.rollback()
                    logging.error(f"IntegrityError while restoring interest '{interest_name}' for user_id: {user_id}. Error: {str(e)}")


    def read(self):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "interest": self.interest
        }
        return data
    

def initInterests():
    """
    The initInterests function creates the Interest table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Interest objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        
        """Tester data for table"""
        interests = [
            Interest(user_id="user123", interest="Music"),
            Interest(user_id="user123", interest="Gaming"),
            Interest(user_id="user456", interest="Traveling"),
            Interest(user_id="user456", interest="Photography"),
        ]
        
        for interest in interests:
            try:
                db.session.add(interest)
                db.session.commit()
                print(f"Record created: {repr(interest)}")
            except IntegrityError:
                '''Fails with bad or duplicate data'''
                db.session.rollback()
                print(f"Record exists, duplicate entry, or error: {interest.interest}")