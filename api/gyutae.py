from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins

# API endpoint to return general data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = [
        {"FirstName": "Gyutae", "LastName": "Kim", "Age": 16, "Email": "gyutae513@gmail.com"},
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
        "Hobbies": ["Soccer", "Sleeping", "Gaming"],
        "Residence": "San Diego"
    }
    return jsonify(gyutae_data)

# Root endpoint to return a simple HTML page
@app.route('/')
def home():
    return """
    <html>
    <head><title>Gyutae's Flask Server</title></head>
    <body>
        <h1>Welcome to Gyutae Kim's Flask Server!</h1>
        <p>Contact me at gyutae513@gmail.com</p>
        <p>Access data at:</p>
        <ul>
            <li><a href="/api/data">/api/data</a></li>
            <li><a href="/api/Gyutae">/api/Gyutae</a></li>
        </ul>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5001)
