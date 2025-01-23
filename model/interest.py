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

    def create(self):
        """
        Add a new interest record to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise Exception(f"Error creating interest: {e}")

    def update(self, new_interest):
        """
        Update the interest record with new data.
        """
        try:
            self.interest = new_interest
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise Exception(f"Error updating interest: {e}")

    def delete(self):
        """
        Delete the interest record from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise Exception(f"Error deleting interest: {e}")

    def read(self):
        """
        Convert the object into a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "interest": self.interest
        }
    
def initInterests():
    """
    Initialize the Interest table with sample data.
    """
    with app.app_context():
        db.create_all()
        interests = [
            Interest(user_id="magic005", interest="Cyber"),
            Interest(user_id="magic005", interest="Film"),
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
                db.session.rollback()
                print(f"Duplicate or error with entry: {interest.interest}")