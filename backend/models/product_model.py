# backend/models/product_model.py
from db import db_connect as db

class Product:
    """Product model for inventory management system."""

    @staticmethod
    def create_table():
        """Create the products table if it doesn't exist."""
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
        cursor.close()
        print("✅ Products table ready.")

    @staticmethod
    def add_product(name, sku, category, quantity, unit_price, supplier_id=None):
        """Insert a new product into the database."""
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO products (name, sku, category, quantity, unit_price, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, sku, category, quantity, unit_price, supplier_id))
        db.commit()
        cursor.close()
        print("✅ Product added successfully!")

    @staticmethod
    def get_all_products():
        """Fetch all products as raw tuples."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return products

    @staticmethod
    def get_all_products_dict():
        """Fetch all products as list of dicts (AI-friendly)."""
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
                "unit_price": float(p[5]),
                "supplier_id": p[6],
                "created_at": str(p[7])
            })
        return result

    @staticmethod
    def get_product_by_id(product_id):
        """Fetch a single product by its ID."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        return product

    @staticmethod
    def update_product(product_id, name=None, sku=None, category=None, quantity=None, unit_price=None, supplier_id=None):
        """Update an existing product."""
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
            return

        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        values.append(product_id)

        cursor.execute(query, tuple(values))
        db.commit()
        cursor.close()
        print("✅ Product updated successfully!")

    @staticmethod
    def delete_product(product_id):
        """Delete a product by ID."""
        cursor = db.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.commit()
        cursor.close()
        print("🗑️ Product deleted successfully!")
