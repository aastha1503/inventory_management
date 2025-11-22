# backend/models/sales_model.py
from db import db_connect as db
import traceback

class SalesModel:
    """Model for storing and querying product sales history."""

    @staticmethod
    def create_table():
        """
        Create the sales_history table with a foreign key to products.
        Safe to run multiple times.
        """
        try:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    qty INT NOT NULL,
                    sale_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            db.commit()

            # Check if foreign key exists
            cursor.execute("""
                SELECT CONSTRAINT_NAME
                FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'sales_history'
                  AND CONSTRAINT_TYPE = 'FOREIGN KEY'
                  AND CONSTRAINT_NAME = 'fk_product';
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    ALTER TABLE sales_history
                    ADD CONSTRAINT fk_product
                    FOREIGN KEY (product_id) REFERENCES products(id)
                    ON DELETE CASCADE;
                """)
                db.commit()

            cursor.close()
            print("✅ sales_history table checked/created.")

        except Exception as e:
            db.rollback()
            print("❌ Error creating sales_history table:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass

    @staticmethod
    def add_sale(product_id, qty, sale_date):
        """Record a sale."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO sales_history (product_id, qty, sale_date)
                VALUES (%s, %s, %s)
            """, (product_id, qty, sale_date))
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            db.rollback()
            print("❌ Error recording sale:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return False

    @staticmethod
    def get_sales_history(product_id, days=None):
        """Get sales history for a product. Optionally filter by last N days."""
        try:
            cursor = db.cursor()
            if days:
                cursor.execute("""
                    SELECT sale_date, qty FROM sales_history
                    WHERE product_id = %s AND sale_date >= (CURDATE() - INTERVAL %s DAY)
                    ORDER BY sale_date ASC
                """, (product_id, days))
            else:
                cursor.execute("""
                    SELECT sale_date, qty FROM sales_history
                    WHERE product_id = %s
                    ORDER BY sale_date ASC
                """, (product_id,))
            rows = cursor.fetchall()
            cursor.close()
            return [{"sale_date": str(r[0]), "qty": int(r[1])} for r in rows]
        except Exception as e:
            print("❌ Error fetching sales history:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return []

    @staticmethod
    def get_total_sales(product_id):
        """Get total quantity sold for a product."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT SUM(qty) FROM sales_history
                WHERE product_id = %s
            """, (product_id,))
            total = cursor.fetchone()[0]
            cursor.close()
            return int(total) if total else 0
        except Exception as e:
            print("❌ Error calculating total sales:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return 0

    @staticmethod
    def get_top_selling_products(limit=5):
        """Get top-selling products by total quantity sold."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.id, p.name, SUM(s.qty) as total_sold
                FROM sales_history s
                JOIN products p ON s.product_id = p.id
                GROUP BY p.id, p.name
                ORDER BY total_sold DESC
                LIMIT %s
            """, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            return [{"product_id": r[0], "product_name": r[1], "total_sold": int(r[2])} for r in rows]
        except Exception as e:
            print("❌ Error fetching top-selling products:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return []

    @staticmethod
    def get_category_wise_sales():
        """Get total sales grouped by product category."""
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.category, SUM(s.qty) as total_qty
                FROM sales_history s
                JOIN products p ON s.product_id = p.id
                GROUP BY p.category
                ORDER BY total_qty DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            return [{"category": r[0], "total_qty": int(r[1])} for r in rows]
        except Exception as e:
            print("❌ Error fetching category-wise sales:", e)
            traceback.print_exc()
            try: cursor.close()
            except: pass
            return []
