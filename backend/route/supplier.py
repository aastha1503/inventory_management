# route/suppliers/supplier.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.supplier_model import Supplier

supplier_bp = Blueprint("suppliers", __name__)

# Create a new supplier
@supplier_bp.route("", methods=["POST"])
@jwt_required()
def add_supplier():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")

    if not name:
        return jsonify({"error": "Supplier name is required"}), 400

    ok = Supplier.add_supplier(name, email, phone, address)
    if ok:
        return jsonify({"message": "Supplier added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add supplier"}), 500


# Get all suppliers
@supplier_bp.route("", methods=["GET"])
@jwt_required()
def get_suppliers():
    suppliers = Supplier.get_all_suppliers()

    result = []
    for s in suppliers:
        result.append({
            "id": s[0],
            "name": s[1],
            "email": s[2],
            "phone": s[3],
            "address": s[4],
            "created_at": str(s[5])
        })
    
    return jsonify(result), 200


# Get supplier by ID
@supplier_bp.route("/<int:supplier_id>", methods=["GET"])
@jwt_required()
def get_supplier_by_id(supplier_id):
    supplier = Supplier.get_supplier_by_id(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    return jsonify(supplier), 200


# Update supplier
@supplier_bp.route("/<int:supplier_id>", methods=["PUT"])
@jwt_required()
def update_supplier(supplier_id):
    data = request.json

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")

    supplier = Supplier.get_supplier_by_id(supplier_id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    ok = Supplier.update_supplier(
        supplier_id=supplier_id,
        name=name,
        email=email,
        phone=phone,
        address=address
    )

    if ok:
        return jsonify({"message": "Supplier updated successfully"}), 200
    else:
        return jsonify({"error": "Supplier update failed"}), 500


# Delete supplier
@supplier_bp.route("/<int:supplier_id>", methods=["DELETE"])
@jwt_required()
def delete_supplier(supplier_id):
    supplier = Supplier.get_supplier_by_id(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    
    result = Supplier.delete_supplier(supplier_id)
    if isinstance(result, dict):
        # our delete_supplier returns dict with success/message
        if not result.get("success", False):
            return jsonify({"error": result.get("message", "Cannot delete supplier")}), 400
        else:
            return jsonify({"message": result.get("message", "Supplier deleted")}), 200

    # fallback (boolean)
    if result:
        return jsonify({"message": "Supplier deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete supplier"}), 500
