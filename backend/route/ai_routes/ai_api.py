# backend/ai_routes/ai_api.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.product_model import Product
from models.sales_model import SalesModel
from ai_engine.forecasting.demand_forecast import DemandForecaster
from ai_engine.forecasting.reorder import ReorderEngine
from ai_engine.forecasting.insights import InventoryInsights

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/forecast/<int:product_id>", methods=["GET"])
@jwt_required()
def forecast(product_id):
    sales_data = SalesModel.get_sales_history(product_id, days=90)  # returns list of (date, qty)
    if not sales_data:
        return jsonify({"error": "No sales history"}), 400

    qty_list = [q for (_d, q) in sales_data]
    preds = DemandForecaster.forecast_next_days(qty_list, n_days=30)
    return jsonify({"product_id": product_id, "predicted_next_30_days": preds})

@ai_bp.route("/reorder/<int:product_id>", methods=["GET"])
@jwt_required()
def reorder(product_id):
    stock = Product.get_stock(product_id)
    if stock is None:
        return jsonify({"error": "Product not found"}), 404

    sales_data = SalesModel.get_sales_history(product_id, days=90)
    qty_list = [q for (_d, q) in sales_data] if sales_data else []

    preds = DemandForecaster.forecast_next_days(qty_list, n_days=30)
    suggestion = ReorderEngine.suggest_reorder(preds, stock)
    suggestion["product_id"] = product_id
    return jsonify(suggestion)

@ai_bp.route("/insights/<int:product_id>", methods=["GET"])
@jwt_required()
def insights(product_id):
    sales_data = SalesModel.get_sales_history(product_id, days=30)
    qty_list = [q for (_d, q) in sales_data] if sales_data else []

    velocity = InventoryInsights.classify_velocity(qty_list)
    anomaly = InventoryInsights.detect_sudden_drop(qty_list)

    return jsonify({
        "product_id": product_id,
        "velocity": velocity,
        "anomaly": anomaly
    })
