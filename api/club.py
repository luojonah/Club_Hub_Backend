from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# Initialize the Flask app
app = Flask(__name__)
# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize SQLAlchemy
db = SQLAlchemy(app)
# Database Model
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topic": self.topic
        }
# Create the database
with app.app_context():
    db.create_all()
# Routes
@app.route('/clubs', methods=['GET'])
def get_clubs():
    """Get all clubs."""
    clubs = Club.query.all()
    return jsonify([club.to_dict() for club in clubs])
@app.route('/clubs', methods=['POST'])
def add_club():
    """Add a new club."""
    data = request.get_json()
    new_club = Club(
        name=data.get('name'),
        description=data.get('description'),
        topic=data.get('topic')
    )
    db.session.add(new_club)
    db.session.commit()
    return jsonify(new_club.to_dict()), 201
@app.route('/clubs/<int:club_id>', methods=['DELETE'])
def delete_club(club_id):
    """Delete a club by ID."""
    club = Club.query.get_or_404(club_id)
    db.session.delete(club)
    db.session.commit()
    return jsonify({"message": "Club deleted successfully!"})
# Run the server
if __name__ == '__main__':
    app.run(debug=True)