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
        for interest_data in data:
            _ = interest_data.pop('id', None)  # Remove 'id' from post_data
            title = interest_data.get("title", None)
            interest = Interest.query.filter_by(_title=title).first()
            if interest:
                interest.update(interest_data)
            else:
                interest = Interest(**interest_data)
                interest.update(interest_data)
                interest.create()

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