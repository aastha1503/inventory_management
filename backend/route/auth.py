from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
from models.user_model import User

auth_bp = Blueprint('auth', __name__)

# -------------------------
# POST /api/auth/signup
# -------------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'staff')  # default role = staff

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    # Check if user already exists
    if User.get_user_by_email(email):
        return jsonify({"error": "User with this email already exists"}), 409

    # Hash password
    hashed_password = generate_password_hash(password)

    try:
        User.add_user(name=name, email=email, password=hashed_password, role=role)
        return jsonify({"message": "✅ User registered successfully!"}), 201
    except Exception as e:
        print("❌ Error creating user:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------
# POST /api/auth/login
# -------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Fetch user from DB
    user = User.get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check password
    if not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Identity must be STRING
    access_token = create_access_token(identity=str(user['id']))

    return jsonify({
        "message": f"Welcome {user['name']}!",
        "role": user['role'],
        "access_token": access_token
    }), 200


# -------------------------
# POST /api/auth/logout
# -------------------------
# No blacklist version → just clear cookies or tell frontend to remove token
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Since JWT tokens are stateless, logout simply means
    clearing cookies (if used) or letting frontend delete the token.
    """
    response = jsonify({"message": "Logged out successfully"})
    
    # Optional → only works if JWT stored in cookies
    unset_jwt_cookies(response)
    
    return response, 200
