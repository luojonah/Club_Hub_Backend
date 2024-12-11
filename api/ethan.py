from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins

# API endpoint to return general data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = [
        {"FirstName": "Ethan", "LastName": "Zhou", "Age": 16, "Email": "ethanz15934@stu.powayusd.com"},
    ]
    return jsonify(data)

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

# Root endpoint to return a simple HTML page
@app.route('/')
def home():
    return """
    <html>
    <head><title>Ethan's Flask Server</title></head>
    <body>
        <h1>Welcome to Ethan's Flask Server!</h1>
        <p>Contact me at ethanz15934@stu.powayusd.com</p>
        <p>Access data at:</p>
        <ul>
            <li><a href="/api/data">/api/data</a></li>
            <li><a href="/api/Ethan">/api/Ethan</a></li>
        </ul>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5001)
