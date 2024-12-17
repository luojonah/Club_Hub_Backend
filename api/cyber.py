from flask import Flask, request, jsonify
import json

app = Flask(__name__)

DATA_FILE = 'cyber_members.json'

# Load members from file
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"members": []}

# Save members to file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/members', methods=['GET'])
def get_members():
    data = load_data()
    return jsonify(data)

@app.route('/members', methods=['POST'])
def add_member():
    data = load_data()
    member = request.json
    data["members"].append(member)
    save_data(data)
    return jsonify({"message": "Member added successfully!", "members": data["members"]})

@app.route('/members/<name>', methods=['DELETE'])
def remove_member(name):
    data = load_data()
    data["members"] = [member for member in data["members"] if member["name"] != name]
    save_data(data)
    return jsonify({"message": "Member removed successfully!", "members": data["members"]})

if __name__ == '__main__':
    app.run(debug=True)
