from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    if not current_user or current_user.role != "admin":
        return jsonify({"code": 403, "msg": "Admin access required"}), 200

    users = User.query.all()
    return jsonify({"code": 200, "data": [u.to_dict() for u in users]})

@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    if not current_user or current_user.role != "admin":
        return jsonify({"code": 403, "msg": "Admin access required"}), 200

    user = User.query.get(user_id)
    if not user:
        return jsonify({"code": 404, "msg": "User not found"}), 200

    data = request.get_json()
    if "status" in data:
        user.status = data["status"]
    if "role" in data:
        user.role = data["role"]

    db.session.commit()
    return jsonify({"code": 200, "msg": "Update successful", "data": user.to_dict()})