# backend/models/product_model.py
from db import db_connect as db
import traceback

class Product:
    """Product model for inventory management system."""

    @staticmethod
    def create_table():
        """Create the products table if it doesn't exist, and try to add FK to suppliers."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    sku VARCHAR(50) UNIQUE,
                    category VARCHAR(100),
                    quantity INT DEFAULT 0,
                    unit_price DECIMAL(10,2) DEFAULT 0.00,
                    supplier_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            db.commit()

            # Try to add foreign key constraint if suppliers table exists and constraint not present
            try:
                # Check if fk already exists
                cursor.execute("""
                    SELECT CONSTRAINT_NAME
                    FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'products'
                      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
                      AND CONSTRAINT_NAME = 'fk_supplier';
                """)
                if not cursor.fetchone():
                    # Add FK (ON DELETE SET NULL so products remain but supplier_id set to NULL)
                    cursor.execute("""
                        ALTER TABLE products
                        ADD CONSTRAINT fk_supplier
                        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
                        ON DELETE SET NULL
                        ON UPDATE CASCADE;
                    """)
                    db.commit()
            except Exception:
                # If alter fails (e.g., suppliers table missing), ignore — FK addition can be retried later.
                db.rollback()

            cursor.close()
            print("✅ Products table ready (with supplier FK if available).")
        except Exception as e:
            db.rollback()
            print("❌ Error creating products table:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass

    @staticmethod
    def supplier_exists(supplier_id):
        """Check whether a supplier exists."""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT id FROM suppliers WHERE id = %s", (supplier_id,))
            exists = cursor.fetchone()
            cursor.close()
            return bool(exists)
        except Exception as e:
            print("❌ Error checking supplier existence:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False

    @staticmethod
    def add_product(name, sku, category, quantity, unit_price, supplier_id=None):
        """Insert a new product into the database. Validates supplier_id if present."""
        try:
            if supplier_id is not None:
                if not Product.supplier_exists(supplier_id):
                    print("❌ add_product failed: supplier does not exist.")
                    return False

            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO products (name, sku, category, quantity, unit_price, supplier_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, sku, category, quantity, unit_price, supplier_id))
            db.commit()
            cursor.close()
            print("✅ Product added successfully!")
            return True
        except Exception as e:
            db.rollback()
            print("❌ Error adding product:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False

    @staticmethod
    def get_all_products():
        """Fetch all products as raw tuples."""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            cursor.close()
            return products
        except Exception as e:
            print("❌ Error fetching products:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return []

    @staticmethod
    def get_all_products_dict():
        """Fetch all products as list of dicts (AI-friendly)."""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            cursor.close()

            result = []
            for p in products:
                result.append({
                    "id": p[0],
                    "name": p[1],
                    "sku": p[2],
                    "category": p[3],
                    "quantity": p[4],
                    "unit_price": float(p[5]) if p[5] is not None else 0.0,
                    "supplier_id": p[6],
                    "created_at": str(p[7])
                })
            return result
        except Exception as e:
            print("❌ Error fetching products dict:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return []

    @staticmethod
    def get_product_by_id(product_id):
        """Fetch a single product by its ID as raw tuple."""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            cursor.close()
            return product
        except Exception as e:
            print("❌ Error fetching product by id:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return None

    @staticmethod
    def get_stock(product_id):
        """Return stock (quantity) of a product."""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Exception as e:
            print("❌ Error fetching stock:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return None

    @staticmethod
    def update_product(product_id, name=None, sku=None, category=None, quantity=None, unit_price=None, supplier_id=None):
        """Update an existing product. Validates supplier_id if provided."""
        try:
            if supplier_id is not None:
                if not Product.supplier_exists(supplier_id):
                    print("❌ update_product failed: supplier does not exist.")
                    return False

            cursor = db.cursor()
            updates = []
            values = []

            if name:
                updates.append("name=%s")
                values.append(name)
            if sku:
                updates.append("sku=%s")
                values.append(sku)
            if category:
                updates.append("category=%s")
                values.append(category)
            if quantity is not None:
                updates.append("quantity=%s")
                values.append(quantity)
            if unit_price is not None:
                updates.append("unit_price=%s")
                values.append(unit_price)
            if supplier_id is not None:
                updates.append("supplier_id=%s")
                values.append(supplier_id)

            if not updates:
                print("⚠ No fields to update.")
                cursor.close()
                return False

            query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
            values.append(product_id)

            cursor.execute(query, tuple(values))
            db.commit()
            cursor.close()
            print("✅ Product updated successfully!")
            return True
        except Exception as e:
            db.rollback()
            print("❌ Error updating product:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False

    @staticmethod
    def delete_product(product_id):
        """Delete a product by ID."""
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            db.commit()
            cursor.close()
            print("🗑️ Product deleted successfully!")
            return True
        except Exception as e:
            db.rollback()
            print("❌ Error deleting product:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False
