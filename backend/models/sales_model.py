# backend/models/sales_model.py
from db import db_connect as db
import traceback

class SalesModel:
    """Model for storing and querying product sales history."""

    @staticmethod
    def create_table():
        """
        Create the sales_history table with a foreign key to products.
        This method is safe to run multiple times.
        """
        try:
            cursor = db.cursor()

            # Step 1: Create table if it doesn't exist
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
            print("✅ sales_history table created (if not exists).")

            # Step 2: Add foreign key if it doesn't already exist
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
                print("✅ Foreign key added successfully.")
            else:
                print("⚠ Foreign key already exists, skipping.")

            cursor.close()

        except Exception as e:
            db.rollback()
            print("❌ Error creating sales_history table:", e)
            try:
                cursor.close()
            except:
                pass

    @staticmethod
    def add_sale(product_id, qty, sale_date):
        """
        Record a sale.
        Args:
            product_id: int, ID of the product
            qty: int, number of units sold
            sale_date: str in 'YYYY-MM-DD' format
        Returns True if inserted successfully, else False
        """
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO sales_history (product_id, qty, sale_date)
                VALUES (%s, %s, %s)
            """, (product_id, qty, sale_date))
            db.commit()
            cursor.close()
            print(f"✅ Sale recorded: product_id={product_id}, qty={qty}, date={sale_date}")
            return True
        except Exception as e:
            db.rollback()
            print("❌ Error recording sale:", e)
            traceback.print_exc()
            try:
                cursor.close()
            except:
                pass
            return False

    @staticmethod
    def get_sales_history(product_id, days=None):
        """
        Get sales history for a product.
        Args:
            product_id: int
            days: int, optional. If provided, fetch only last N days.
        Returns:
            List of tuples: [(sale_date, qty), ...]
        """
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
            return [(str(r[0]), int(r[1])) for r in rows]
        except Exception as e:
            print("❌ Error fetching sales history:", e)
            try:
                cursor.close()
            except:
                pass
            return []

    @staticmethod
    def get_total_sales(product_id):
        """
        Get total quantity sold for a product.
        Returns integer sum of qty.
        """
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
            try:
                cursor.close()
            except:
                pass
            return 0
