from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    club_name = db.Column(db.String(100), db.ForeignKey('club.name'), nullable=False)
