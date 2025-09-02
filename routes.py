from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt,
    set_access_cookies, unset_jwt_cookies
)
from models import db, User

auth_bp = Blueprint('auth', __name__)

# -------------------
# Register Route
# -------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201


# -------------------
# Login Route
# -------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Fix: identity must be string; role in additional_claims
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )
        response = jsonify({"msg": "Login successful"})
        set_access_cookies(response, access_token)
        return response
    return jsonify({"msg": "Invalid credentials"}), 401


# -------------------
# Protected Route
# -------------------
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    role = get_jwt()["role"]
    return jsonify({"msg": f"Hello user {user_id} with role {role}"})


# -------------------
# Admin Route
# -------------------
@auth_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    user_id = get_jwt_identity()
    role = get_jwt()["role"]
    if role != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    return jsonify({"msg": "Welcome, admin!"})


# -------------------
# Logout Route
# -------------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "Logged out"})
    unset_jwt_cookies(response)
    return response
