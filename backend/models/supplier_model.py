# backend/models/supplier_model.py
from db import db_connect as db
import traceback

class Supplier:
    """Supplier model for inventory management."""

    @staticmethod
    def create_table():
        """Create the suppliers table if it does not exist."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    phone VARCHAR(20),
                    address VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            db.commit()
            cursor.close()
            print("✅ Suppliers table created (or already exists).")
        except Exception as e:
            db.rollback()
            print("❌ Error creating suppliers table:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass

    @staticmethod
    def add_supplier(name, email=None, phone=None, address=None):
        """Insert a new supplier into the database."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO suppliers (name, email, phone, address)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, address))
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            db.rollback()
            print("❌ Error adding supplier:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False

    @staticmethod
    def get_all_suppliers():
        """Fetch all suppliers as raw tuples."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, name, email, phone, address, created_at 
                FROM suppliers
            """)
            suppliers = cursor.fetchall()
            cursor.close()
            return suppliers
        except Exception as e:
            print("❌ Error fetching suppliers:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return []

    @staticmethod
    def get_supplier_by_id(supplier_id):
        """Fetch a supplier by ID. Returns dict or None."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, name, email, phone, address, created_at 
                FROM suppliers 
                WHERE id = %s
            """, (supplier_id,))
            supplier = cursor.fetchone()
            cursor.close()

            if not supplier:
                return None
            
            return {
                "id": supplier[0],
                "name": supplier[1],
                "email": supplier[2],
                "phone": supplier[3],
                "address": supplier[4],
                "created_at": supplier[5]
            }
        except Exception as e:
            print("❌ Error fetching supplier:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return None

    @staticmethod
    def update_supplier(supplier_id, name=None, email=None, phone=None, address=None):
        """Update supplier details (any field)."""
        try:
            cursor = db.cursor()

            updates = []
            values = []

            if name:
                updates.append("name = %s")
                values.append(name)
            if email:
                updates.append("email = %s")
                values.append(email)
            if phone:
                updates.append("phone = %s")
                values.append(phone)
            if address:
                updates.append("address = %s")
                values.append(address)

            if not updates:
                # nothing to update
                cursor.close()
                return False

            query = f"UPDATE suppliers SET {', '.join(updates)} WHERE id = %s"
            values.append(supplier_id)

            cursor.execute(query, tuple(values))
            db.commit()
            cursor.close()
            return True

        except Exception as e:
            db.rollback()
            print("❌ Error updating supplier:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False

    @staticmethod
    def delete_supplier(supplier_id):
        """
        Delete a supplier by ID.
        Safe delete: if products are linked, returns a dict indicating failure.
        """
        try:
            cursor = db.cursor()

            # Check if supplier has linked products
            cursor.execute("SELECT COUNT(*) FROM products WHERE supplier_id = %s", (supplier_id,))
            count_row = cursor.fetchone()
            count = count_row[0] if count_row else 0

            if count > 0:
                cursor.close()
                return {
                    "success": False,
                    "message": "Cannot delete supplier. Some products are linked to this supplier."
                }

            cursor.execute("DELETE FROM suppliers WHERE id = %s", (supplier_id,))
            db.commit()
            cursor.close()
            return {"success": True, "message": "Supplier deleted successfully."}

        except Exception as e:
            db.rollback()
            print("❌ Error deleting supplier:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return {"success": False, "message": "Internal server error"}
