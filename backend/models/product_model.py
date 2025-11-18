# models/product_model.py
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
            );
        """)
        db.commit()
        cursor.close()

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
        """Fetch all products."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return products

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

        # Build dynamic SQL for only provided fields
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
            print(" No fields to update.")
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
