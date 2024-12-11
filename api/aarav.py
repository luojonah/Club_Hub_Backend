from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins

# API endpoint to return general data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = [
        {"FirstName": "Aarav", "LastName": "Sonara", "Age": 15, "Email": "sonara.aarav@gmail.com"},
    ]
    return jsonify(data)

# API endpoint specific to Aarav
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
    <head><title>Aarav's Flask Server</title></head>
    <body>
        <h1>Welcome to Aarav's Flask Server!</h1>
        <p>Contact me at sonara.aarav@gmail.com</p>
        <p>Access data at:</p>
        <ul>
            <li><a href="/api/data">/api/data</a></li>
            <li><a href="/api/Aarav">/api/Aarav</a></li>
        </ul>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5001)
