from flask import Blueprint, request, jsonify
from model import db, Member

robotics_bp = Blueprint('robotics', __name__)

# Fetch all Robotics Club members
@robotics_bp.route('/clubs/robotics/members', methods=['GET'])
def get_robotics_members():
    members = Member.query.filter_by(club_name="Robotics Club").all()
    return jsonify([{"name": m.name, "role": m.role} for m in members])

# Add a new member to Robotics Club
@robotics_bp.route('/clubs/robotics/members', methods=['POST'])
def add_robotics_member():
    data = request.get_json()
    name = data.get("name")
    role = data.get("role")

    if not name or not role:
        return jsonify({"error": "Name and role are required!"}), 400

    new_member = Member(name=name, role=role, club_name="Robotics Club")
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"success": True, "name": name, "role": role})
