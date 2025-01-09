from __init__ import db

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
        # Clear existing interests
        Interest.query.filter_by(user_id=user_id).delete()
        # Add new interests
        for interest in interests:
            db.session.add(Interest(user_id, interest))
        db.session.commit()
