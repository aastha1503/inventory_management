from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.sales_model import SalesModel

sales_bp = Blueprint("sales", __name__)

# -------------------------
# POST /api/sales → Record a sale
# -------------------------
@sales_bp.route("", methods=["POST"])
@jwt_required()
def add_sale():
    data = request.get_json()

    product_id = data.get("product_id")
    qty = data.get("qty")
    sale_date = data.get("sale_date")  # format: 'YYYY-MM-DD'

    if not product_id or not qty or not sale_date:
        return jsonify({"error": "product_id, qty, and sale_date are required"}), 400

    success = SalesModel.add_sale(product_id, qty, sale_date)
    if success:
        return jsonify({"message": f"✅ Sale recorded for product {product_id}"}), 201
    else:
        return jsonify({"error": "Failed to record sale"}), 500


# -------------------------
# GET /api/sales/<product_id> → Get sales history
# Optional query param: ?days=N
# -------------------------
@sales_bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_sales(product_id):
    days = request.args.get("days", default=None, type=int)

    history = SalesModel.get_sales_history(product_id, days)
    if not history:
        return jsonify({"message": "No sales found"}), 404

    return jsonify({"product_id": product_id, "sales_history": history}), 200


# -------------------------
# GET /api/sales/<product_id>/total → Get total sales
# -------------------------
@sales_bp.route("/<int:product_id>/total", methods=["GET"])
@jwt_required()
def get_total_sales(product_id):
    total = SalesModel.get_total_sales(product_id)
    return jsonify({"product_id": product_id, "total_sales": total}), 200
