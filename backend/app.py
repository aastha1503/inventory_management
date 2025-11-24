from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS

from route.auth import auth_bp
from route.items import item_bp
from route.sales import sales_bp
from route.ai_routes.ai_api import ai_bp
from route.supplier import supplier_bp


from models.product_model import Product
from models.sales_model import SalesModel
from models.user_model import User
from models.supplier_model import Supplier


import os
import sys

load_dotenv()

app = Flask(__name__)

# Enable CORS for Android access
CORS(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

jwt = JWTManager(app)

@jwt.unauthorized_loader
def handle_missing_token(err):
    return jsonify({"error": "Missing or invalid access token"}), 401

@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

# Routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(item_bp, url_prefix="/api/items")
app.register_blueprint(sales_bp, url_prefix="/api/sales")
app.register_blueprint(ai_bp, url_prefix="/api/ai")
app.register_blueprint(supplier_bp, url_prefix="/api/suppliers")


print("📌 Creating database tables...")
User.create_table()
Product.create_table()
SalesModel.create_table()
Supplier.create_table()
print("✅ Tables created successfully!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
