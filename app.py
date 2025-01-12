from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins

# API endpoint to return general data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = [
        {"FirstName": "Club", "LastName": "Hub", "Age": 0.05, "Email": "N/A"},
    ]
    return jsonify(data)

# API endpoint specific to Gyutae
@app.route('/api/Gyutae', methods=['GET'])
def get_gyutae():
    gyutae_data = {
        "FirstName": "Gyutae",
        "LastName": "Kim",
        "Age": 16,
        "Email": "gyutae513@gmail.com",
        "Hobbies": ["Soccer", "Coding", "Gaming"],
        "Residence": "San Diego"
    }
    return jsonify(gyutae_data)

# API endpoint specific to Ansh Kumar
@app.route('/api/Ansh', methods=['GET'])
def get_ansh():
    ansh_data = {
        "FirstName": "Ansh",
        "LastName": "Kumar",
        "Age": 15,
        "Email": "anshie09@gmail.com",
        "Hobbies": ["Basketball", "Reading", "Coding"],
        "Residence": "San Diego"
    }
    return jsonify(ansh_data)

# API endpoint specific to Ethan
@app.route('/api/Ethan', methods=['GET'])
def get_ethan():
    ethan_data = {
        "FirstName": "Ethan",
        "LastName": "Zhou",
        "Age": 16,
        "Email": "ethanz15934@stu.powayusd.com",
        "Hobbies": ["Eating", "Sleeping", "Cooking"],
        "Residence": "San Diego"
    }
    return jsonify(ethan_data)


# API endpoint specific to Jonah
@app.route('/api/Jonah', methods=['GET'])
def get_jonah():
    jonah_data = {
        "FirstName": "Jonah",
        "LastName": "Luo",
        "Age": 15,
        "Email": "jonahluo22@gmail.com",
        "Hobbies": ["Soccer", "Movies", "Hiking", "Camping"],
        "Residence": "San Diego"
    }
    return jsonify(jonah_data)

@app.route('/api/Aarav', methods=['GET'])
def get_Aarav():
    Aarav_data = {
        "FirstName": "Aarav",
        "LastName": "Sonara",
        "Age": 15,
        "Email": "sonara.aarav@gmail.com",
        "Hobbies": ["Basketball", "Sleeping", "Gaming"],
        "Residence": "San Diego"
    }
    return jsonify(Aarav_data)

# Root endpoint to return a simple HTML page
@app.route('/')
def home():
    return """
    <html>
    <head><title>Club Hub Flask Server</title></head>
    <body>
        <h1>Welcome to the Club Hub Flask Server!</h1>
        <p>Access data at:</p>
        <ul>
            <li><a href="/api/data">/api/data</a></li>
            <li><a href="/api/Gyutae">/api/Gyutae</a></li>
            <li><a href="/api/Ansh">/api/Ansh</a></li>
            <li><a href="/api/Jonah">/api/Jonah</a></li>
            <li><a href="/api/Aarav">/api/Aarav</a></li>
            <li><a href="/api/Ethan">/api/Ethan</a></li>
        </ul>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5001)
    from flask import Flask
from model import db
from cyber import cyber_bp
from robotics import robotics_bp

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubhub.db'  # Adjust database path as needed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/volumes/user_management.db'

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(cyber_bp, url_prefix="/api")
app.register_blueprint(robotics_bp, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if they don't already exist
    app.run(debug=True)


