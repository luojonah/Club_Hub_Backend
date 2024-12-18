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
    member_count = db.Column(db.Integer, nullable=False, default=0)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "topic": self.topic,
            "member_count": self.member_count
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
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        # Validate input data
        if not all(key in data for key in ('name', 'description', 'topic')):
            return jsonify({"error": "Missing required fields: name, description, topic"}), 400
        # Create a new Club instance
        new_club = Club(
            name=data['name'],
            description=data['description'],
            topic=data['topic'],
            member_count=data.get('member_count', 0)  # Default to 0 if not provided
        )
        db.session.add(new_club)
        db.session.commit()
        return jsonify(new_club.to_dict()), 201
    except Exception as e:
        return jsonify({"error": "Invalid JSON or server error", "details": str(e)}), 500

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