from datetime import datetime
from __init__ import db
from flask_sqlalchemy import SQLAlchemy




class Event(db.Model):
    __tablename__ = 'event1'  # Table name is 'event1'


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)


    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        self.date = datetime.strptime(date, '%Y-%m-%d')


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d')
        }


    @classmethod
    def create(cls, title, description, date):
        new_event = cls(title=title, description=description, date=date)
        db.session.add(new_event)
        db.session.commit()
        return new_event




    @classmethod
    def delete(cls, event_id):
        event = cls.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return True
        return False