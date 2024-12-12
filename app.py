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
        "Age": 17,
        "Email": "ansh.kumar@example.com",
        "Hobbies": ["Basketball", "Reading", "Coding"],
        "Residence": "San Diego"
    }
    return jsonify(ansh_data)

# API endpoint to return general data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = [
        {"FirstName": "Jonah", "LastName": "Luo", "Age": 15, "Email": "jonahluo22@gmail.com"},
    ]
    return jsonify(data)

# API endpoint specific to Gyutae
@app.route('/api/Jonah', methods=['GET'])
def get_gyutae():
    gyutae_data = {
        "FirstName": "Jonah",
        "LastName": "Luo",
        "Age": 15,
        "Email": "jonahluo22@gmail.com",
        "Hobbies": ["Soccer", "Movies", "Hiking", "Camping"],
        "Residence": "San Diego"
    }
    return jsonify(gyutae_data)

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
        </ul>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5001)