import sqlite3
import os

class Database:
    def __init__(self):
        self.db_file = "invoice_system.db"
        self.conn = self.create_connection()
        self.create_tables()
        
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None
            
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            
            # Create customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create products table with additional columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    wholesale_price REAL,
                    retail_price REAL,
                    base_unit TEXT,
                    alt_unit TEXT,
                    unit_ratio REAL DEFAULT 1,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create invoices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    total_amount REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Create invoice_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER,
                    product_id INTEGER,
                    quantity REAL,
                    price_type TEXT,
                    unit_price REAL,
                    total_price REAL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # Add any missing columns to existing tables
            try:
                # Add email column to customers if it doesn't exist
                cursor.execute("ALTER TABLE customers ADD COLUMN email TEXT")
            except sqlite3.OperationalError:
                # Column already exists
                pass
                
            try:
                # Add alt_unit column to products if it doesn't exist
                cursor.execute("ALTER TABLE products ADD COLUMN alt_unit TEXT")
            except sqlite3.OperationalError:
                pass
                
            try:
                # Add unit_ratio column to products if it doesn't exist
                cursor.execute("ALTER TABLE products ADD COLUMN unit_ratio REAL DEFAULT 1")
            except sqlite3.OperationalError:
                pass
                
            try:
                # Add description column to products if it doesn't exist
                cursor.execute("ALTER TABLE products ADD COLUMN description TEXT")
            except sqlite3.OperationalError:
                pass
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            
    def close(self):
        if self.conn:
            self.conn.close()
