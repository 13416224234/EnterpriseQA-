import hashlib
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"code": 400, "msg": "Username and password cannot be empty"}), 200

    md5_password = hashlib.md5(password.encode()).hexdigest()
    user = User.query.filter_by(username=username, password=md5_password).first()

    if not user:
        return jsonify({"code": 401, "msg": "Invalid username or password"}), 200

    if user.status == 0:
        return jsonify({"code": 403, "msg": "Account disabled, please contact admin"}), 200

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
            "username": user.username
        }
    )

    return jsonify({
        "code": 200,
        "msg": "Login successful",
        "data": {
            "token": token,
            "user": user.to_dict()
        }
    })

@auth_bp.route("/info", methods=["GET"])
@jwt_required()
def get_user_info():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"code": 404, "msg": "User not found"}), 200
    return jsonify({"code": 200, "data": user.to_dict()})

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    email = data.get("email", "").strip()
    real_name = data.get("real_name", "").strip()

    if not username or not password:
        return jsonify({"code": 400, "msg": "Username and password cannot be empty"}), 200

    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "msg": "Username already exists"}), 200

    md5_password = hashlib.md5(password.encode()).hexdigest()
    user = User(
        username=username,
        password=md5_password,
        email=email,
        real_name=real_name,
        role="user"
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"code": 200, "msg": "Registration successful", "data": user.to_dict()})