from datetime import datetime
from __init__ import db


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
