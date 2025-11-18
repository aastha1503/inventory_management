from flask import Flask, jsonify
from route.auth import auth_bp
from route.items import item_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models.product_model import Product
import os

# Load .env file
load_dotenv()

app = Flask(__name__)


#  JWT CONFIGURATION
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")   # from .env
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600                # 1 hour expiry

jwt = JWTManager(app)

# Optional JWT error handlers (recommended)
@jwt.unauthorized_loader
def handle_missing_token(err):
    return jsonify({"error": "Missing or invalid access token"}), 401

@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

#  REGISTER BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(item_bp, url_prefix="/api/items")

print(app.url_map)


if __name__ == "__main__":
    app.run(debug=True)
