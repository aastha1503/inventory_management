from db import db_connect as db

class User: 
    """User model for inventory management."""
    @staticmethod
    def create_table():
        """Create the users table if it doesn't exist."""
        try:
            with db.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role ENUM('admin', 'manager', 'staff') DEFAULT 'staff',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            db.commit()
            print("Users table created (or already exists).")
        except Exception as e:
            db.rollback()  # revert changes if something goes wrong
            print(" Error creating users table:", e)
        finally:
            cursor.close()


    @staticmethod
    def add_user(name, email, password, role='staff'):
        """Insert a new user into the database."""
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, role))
        db.commit()
        cursor.close()
 
    @staticmethod
    def get_all_users():
        """Fetch all users."""
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email, role, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        return users
       

    @staticmethod
    def get_user_by_email(email):
        """Fetch a user by email."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if not user :
            return None
        return {
            "id" : user[0],
            "name" : user[1],
            "email" : user[2],
            "password" : user[3],
            "role" : user[4],
            "created_at" : user[5]
        }
        

    @staticmethod
    def delete_user(user_id):
        """Delete a user by ID."""
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
        cursor.close()
