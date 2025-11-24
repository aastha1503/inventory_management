from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.product_model import Product
from models.supplier_model import Supplier    # <-- REQUIRED for supplier validation

item_bp = Blueprint("items", __name__)



# CREATE PRODUCT
@item_bp.route("", methods=["POST"])
@jwt_required()
def create_item():
    data = request.get_json()
    print("Received JSON:", data)

    name = data.get("name")
    sku = data.get("sku")
    category = data.get("category")
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")
    supplier_id = data.get("supplier_id")

    # Required fields
    if not name or not sku:
        return jsonify({"message": "Name and SKU are required"}), 400

    # Validate supplier
    if supplier_id is not None:
        supplier = Supplier.get_supplier_by_id(supplier_id)
        if not supplier:
            return jsonify({"error": "Invalid supplier_id. Supplier does not exist"}), 400

    try:
        Product.add_product(name, sku, category, quantity, unit_price, supplier_id)
        return jsonify({"message": "✅ Product added successfully!"}), 201
    except Exception as e:
        print("❌ Error adding product:", e)
        return jsonify({"error": str(e)}), 500



# GET ALL PRODUCTS
@item_bp.route("", methods=["GET"])
@jwt_required()
def get_all_items():
    try:
        products = Product.get_all_products()
        result = []

        for p in products:
            result.append({
                "id": p[0],
                "name": p[1],
                "sku": p[2],
                "category": p[3],
                "quantity": p[4],
                "unit_price": float(p[5]),
                "supplier_id": p[6],
                "created_at": str(p[7])
            })

        return jsonify(result), 200

    except Exception as e:
        print("❌ Error fetching products:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------
# GET PRODUCT BY ID
# -----------------------------------
@item_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    try:
        product = Product.get_product_by_id(item_id)

        if not product:
            return jsonify({"message": "Product not found"}), 404

        p = product

        return jsonify({
            "id": p[0],
            "name": p[1],
            "sku": p[2],
            "category": p[3],
            "quantity": p[4],
            "unit_price": float(p[5]),
            "supplier_id": p[6],
            "created_at": str(p[7])
        }), 200

    except Exception as e:
        print("❌ Error fetching product:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------
# UPDATE PRODUCT
# -----------------------------------
@item_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    data = request.get_json()

    supplier_id = data.get("supplier_id")

    # Validate supplier before updating
    if supplier_id is not None:
        supplier = Supplier.get_supplier_by_id(supplier_id)
        if not supplier:
            return jsonify({"error": "Invalid supplier_id. Supplier does not exist"}), 400

    try:
        Product.update_product(
            product_id=item_id,
            name=data.get("name"),
            sku=data.get("sku"),
            category=data.get("category"),
            quantity=data.get("quantity"),
            unit_price=data.get("unit_price"),
            supplier_id=supplier_id
        )
        return jsonify({"message": "✅ Product updated successfully!"}), 200

    except Exception as e:
        print("❌ Error updating product:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------
# DELETE PRODUCT
# -----------------------------------
@item_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    try:
        Product.delete_product(item_id)
        return jsonify({"message": "🗑 Product deleted successfully!"}), 200

    except Exception as e:
        print("❌ Error deleting product:", e)
        return jsonify({"error": str(e)}), 500
