from flask import Blueprint, request, jsonify
from model import db, Member

cyber_bp = Blueprint('cyber', __name__)

# Fetch all Cyber Club members
@cyber_bp.route('/clubs/cyber/members', methods=['GET'])
def get_cyber_members():
    members = Member.query.filter_by(club_name="Cyber Club").all()
    return jsonify([{"name": m.name, "role": m.role} for m in members])

# Add a new member to Cyber Club
@cyber_bp.route('/clubs/cyber/members', methods=['POST'])
def add_cyber_member():
    data = request.get_json()
    name = data.get("name")
    role = data.get("role")

    if not name or not role:
        return jsonify({"error": "Name and role are required!"}), 400

    new_member = Member(name=name, role=role, club_name="Cyber Club")
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"success": True, "name": name, "role": role})
