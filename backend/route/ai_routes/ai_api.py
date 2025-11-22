# backend/ai_routes/ai_api.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.product_model import Product
from models.sales_model import SalesModel
from ai_engine.forecasting.demand_forecast import DemandForecaster
from ai_engine.forecasting.reorder import ReorderEngine
from ai_engine.forecasting.insights import InventoryInsights

ai_bp = Blueprint("ai", __name__)

# -----------------------------
# EXISTING ROUTES (unchanged)
# -----------------------------

@ai_bp.route("/forecast/<int:product_id>", methods=["GET"])
@jwt_required()
def forecast(product_id):
    sales_data = SalesModel.get_sales_history(product_id, days=90)
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

# ---------------------------------------------------------
# NEW ROUTES FOR ANDROID CHARTS
# ---------------------------------------------------------

# 1️⃣ Daily Sales Line Chart API
@ai_bp.route("/charts/daily_sales/<int:product_id>", methods=["GET"])
@jwt_required()
def daily_sales_chart(product_id):
    sales = SalesModel.get_sales_history(product_id, days=30)
    
    if not sales:
        return jsonify({"error": "No sales history"}), 400

    dates = [str(d) for (d, _q) in sales]
    quantities = [q for (_d, q) in sales]

    return jsonify({
        "product_id": product_id,
        "dates": dates,
        "quantities": quantities
    })


# 2️⃣ Category-wise Sales Pie Chart API
@ai_bp.route("/charts/category_sales", methods=["GET"])
@jwt_required()
def category_sales_chart():
    category_sales = SalesModel.get_category_wise_sales()  
    # returns dict: {"Electronics": 120, "Clothing": 80, ...}

    return jsonify(category_sales)


# 3️⃣ Top 5 Best Selling Products - Bar Chart API
@ai_bp.route("/charts/top_products", methods=["GET"])
@jwt_required()
def top_products_chart():
    top_products = SalesModel.get_top_selling_products(limit=5)
    # returns list of tuples: [(product_name, qty), ...]

    names = [p[0] for p in top_products]
    qty = [p[1] for p in top_products]

    return jsonify({
        "product_names": names,
        "quantities": qty
    })


# 4️⃣ Stock Levels Bar Chart API
@ai_bp.route("/charts/stock_levels", methods=["GET"])
@jwt_required()
def stock_levels_chart():
    stock_data = Product.get_all_stock()
    # returns list of tuples: [(product_name, stock_qty), ...]

    names = [p[0] for p in stock_data]
    stock = [p[1] for p in stock_data]

    return jsonify({
        "product_names": names,
        "stock": stock
    })
