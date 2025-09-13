#!/usr/bin/env python3
"""
Fast MySQL Database Setup Script

This script creates a MySQL database with:
- Smaller dataset for quick testing (thousands of rows)
- Intentionally slow queries for testing
- Missing indexes to demonstrate optimization
- Realistic data patterns
"""

import mysql.connector
import random
import time
from datetime import datetime, timedelta
import json

class FastMySQLSetup:
    """Fast setup MySQL database with test data."""
    
    def __init__(self, host='localhost', port=3306, user='root', password=''):
        """Initialize database connection."""
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': 'observability_test'
        }
        self.connection = None
    
    def connect(self):
        """Connect to MySQL server."""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password']
            )
            print("✅ Connected to MySQL server")
            return True
        except mysql.connector.Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def create_database(self):
        """Create the test database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP DATABASE IF EXISTS observability_test")
            cursor.execute("CREATE DATABASE observability_test")
            cursor.execute("USE observability_test")
            print("✅ Created database 'observability_test'")
            return True
        except mysql.connector.Error as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    def create_tables(self):
        """Create tables with realistic structure."""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    age INT,
                    city VARCHAR(100),
                    country VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    profile_data JSON
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE products (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    category_id INT,
                    price DECIMAL(10,2),
                    in_stock BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    metadata JSON
                )
            """)
            
            # Orders table
            cursor.execute("""
                CREATE TABLE orders (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    total_amount DECIMAL(10,2),
                    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled'),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    shipping_address TEXT,
                    payment_method VARCHAR(50)
                )
            """)
            
            # Order items table
            cursor.execute("""
                CREATE TABLE order_items (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    order_id INT,
                    product_id INT,
                    quantity INT,
                    price DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Posts table
            cursor.execute("""
                CREATE TABLE posts (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    title VARCHAR(255),
                    content TEXT,
                    published BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    view_count INT DEFAULT 0
                )
            """)
            
            # Logs table
            cursor.execute("""
                CREATE TABLE logs (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    log_level ENUM('DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'),
                    message TEXT,
                    user_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSON
                )
            """)
            
            print("✅ Created all tables")
            return True
            
        except mysql.connector.Error as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def generate_sample_data(self):
        """Generate realistic sample data (smaller dataset)."""
        print("🔄 Generating sample data (fast version)...")
        
        cursor = self.connection.cursor()
        
        # Sample data lists
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
                 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
                 'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis',
                 'Seattle', 'Denver', 'Washington', 'Boston', 'El Paso', 'Nashville',
                 'Detroit', 'Oklahoma City', 'Portland', 'Las Vegas', 'Memphis', 'Louisville']
        
        countries = ['USA', 'Canada', 'Mexico', 'UK', 'Germany', 'France', 'Italy', 'Spain',
                    'Australia', 'Japan', 'China', 'India', 'Brazil', 'Argentina']
        
        product_categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports',
                             'Beauty', 'Toys', 'Automotive', 'Health', 'Food']
        
        product_names = ['Laptop', 'Smartphone', 'Headphones', 'Tablet', 'Camera', 'Watch',
                        'Shoes', 'Shirt', 'Jeans', 'Jacket', 'Book', 'Notebook', 'Pen',
                        'Chair', 'Table', 'Lamp', 'Plant', 'Tool', 'Game', 'Toy']
        
        log_messages = [
            'User login successful', 'Database connection established', 'Query executed',
            'File uploaded', 'Email sent', 'Payment processed', 'Order created',
            'User registered', 'Password changed', 'Profile updated', 'Search performed',
            'Error occurred', 'Warning generated', 'Debug information', 'System started'
        ]
        
        # Generate users (10K records)
        print("  📊 Generating 10,000 users...")
        users_data = []
        for i in range(10000):
            users_data.append((
                f"user{i}@example.com",
                f"User {i}",
                random.randint(18, 80),
                random.choice(cities),
                random.choice(countries),
                datetime.now() - timedelta(days=random.randint(1, 365)),
                datetime.now() - timedelta(days=random.randint(0, 30)),
                random.choice([True, False]),
                json.dumps({"preferences": {"theme": "dark", "notifications": True}})
            ))
        
        cursor.executemany("""
            INSERT INTO users (email, name, age, city, country, created_at, last_login, is_active, profile_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, users_data)
        self.connection.commit()
        
        # Generate products (5K records)
        print("  📊 Generating 5,000 products...")
        products_data = []
        for i in range(5000):
            products_data.append((
                f"{random.choice(product_names)} {i}",
                f"Description for product {i}",
                random.randint(1, len(product_categories)),
                round(random.uniform(10, 1000), 2),
                random.choice([True, False]),
                datetime.now() - timedelta(days=random.randint(1, 365)),
                json.dumps({"brand": f"Brand{i%100}", "rating": round(random.uniform(1, 5), 1)})
            ))
        
        cursor.executemany("""
            INSERT INTO products (name, description, category_id, price, in_stock, created_at, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, products_data)
        self.connection.commit()
        
        # Generate orders (20K records)
        print("  📊 Generating 20,000 orders...")
        orders_data = []
        for i in range(20000):
            orders_data.append((
                random.randint(1, 10000),
                round(random.uniform(10, 5000), 2),
                random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
                datetime.now() - timedelta(days=random.randint(1, 365)),
                f"Address {i}",
                random.choice(['credit_card', 'paypal', 'bank_transfer'])
            ))
        
        cursor.executemany("""
            INSERT INTO orders (user_id, total_amount, status, created_at, shipping_address, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, orders_data)
        self.connection.commit()
        
        # Generate order items (50K records)
        print("  📊 Generating 50,000 order items...")
        order_items_data = []
        for i in range(50000):
            order_items_data.append((
                random.randint(1, 20000),
                random.randint(1, 5000),
                random.randint(1, 10),
                round(random.uniform(5, 500), 2)
            ))
        
        cursor.executemany("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, order_items_data)
        self.connection.commit()
        
        # Generate posts (10K records)
        print("  📊 Generating 10,000 posts...")
        posts_data = []
        for i in range(10000):
            posts_data.append((
                random.randint(1, 10000),
                f"Post Title {i}",
                f"This is the content of post {i}. " * random.randint(5, 20),
                random.choice([True, False]),
                datetime.now() - timedelta(days=random.randint(1, 365)),
                random.randint(0, 10000)
            ))
        
        cursor.executemany("""
            INSERT INTO posts (user_id, title, content, published, created_at, view_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, posts_data)
        self.connection.commit()
        
        # Generate logs (100K records)
        print("  📊 Generating 100,000 log entries...")
        logs_data = []
        for i in range(100000):
            logs_data.append((
                random.choice(['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']),
                random.choice(log_messages),
                random.randint(1, 10000),
                datetime.now() - timedelta(days=random.randint(1, 30)),
                json.dumps({"request_id": f"req_{i}", "duration": random.randint(1, 1000)})
            ))
        
        cursor.executemany("""
            INSERT INTO logs (log_level, message, user_id, created_at, metadata)
            VALUES (%s, %s, %s, %s, %s)
        """, logs_data)
        self.connection.commit()
        
        print("✅ Sample data generation complete!")
    
    def create_slow_queries(self):
        """Create intentionally slow queries for testing."""
        print("🐌 Creating slow query examples...")
        
        cursor = self.connection.cursor()
        
        # Create some indexes to make some queries fast, but leave others slow
        cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX idx_orders_user_id ON orders(user_id)")
        cursor.execute("CREATE INDEX idx_products_category_id ON products(category_id)")
        cursor.execute("CREATE INDEX idx_logs_created_at ON logs(created_at)")
        
        print("✅ Created some indexes (leaving others missing for slow queries)")
        
        # Create a view with slow query examples
        cursor.execute("""
            CREATE VIEW slow_queries_examples AS
            SELECT 
                'Missing Index Query' as query_type,
                'SELECT * FROM users WHERE city = ''New York'' AND age > 25' as query_text,
                'Missing composite index on (city, age)' as issue
            UNION ALL
            SELECT 
                'Full Table Scan Query',
                'SELECT * FROM products WHERE name LIKE ''%laptop%''',
                'LIKE with leading wildcard prevents index usage'
            UNION ALL
            SELECT 
                'Inefficient JOIN Query',
                'SELECT u.*, p.* FROM users u LEFT JOIN posts p ON u.id = p.user_id WHERE u.created_at > ''2024-01-01''',
                'Missing indexes on created_at and user_id'
            UNION ALL
            SELECT 
                'Subquery Performance Issue',
                'SELECT COUNT(*) FROM orders o WHERE EXISTS (SELECT 1 FROM order_items oi WHERE oi.order_id = o.id AND oi.quantity > 10)',
                'EXISTS subquery not optimized, should use JOIN'
            UNION ALL
            SELECT 
                'GROUP BY Without Index',
                'SELECT user_id, COUNT(*) as post_count FROM posts GROUP BY user_id HAVING post_count > 10',
                'GROUP BY without proper indexing'
        """)
        
        print("✅ Created slow query examples view")
    
    def update_config(self):
        """Update the observability tool config with the new database."""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            config['mysql']['database'] = 'observability_test'
            config['mysql']['host'] = self.config['host']
            config['mysql']['port'] = self.config['port']
            config['mysql']['user'] = self.config['user']
            config['mysql']['password'] = self.config['password']
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ Updated config.json with new database settings")
            
        except Exception as e:
            print(f"❌ Error updating config: {e}")
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

def main():
    """Main setup function."""
    print("🚀 Fast MySQL Database Setup for Observability Testing")
    print("="*60)
    
    # Get database connection details
    print("Enter your MySQL connection details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = int(input("Port (default: 3306): ").strip() or "3306")
    user = input("Username (default: root): ").strip() or "root"
    password = input("Password: ").strip()
    
    # Initialize setup
    setup = FastMySQLSetup(host, port, user, password)
    
    if not setup.connect():
        return
    
    try:
        # Create database and tables
        if not setup.create_database():
            return
        
        if not setup.create_tables():
            return
        
        # Generate sample data
        setup.generate_sample_data()
        
        # Create slow queries
        setup.create_slow_queries()
        
        # Update config
        setup.update_config()
        
        print("\n" + "="*60)
        print("🎉 FAST DATABASE SETUP COMPLETE!")
        print("="*60)
        print("Your MySQL database is now ready with:")
        print("✅ 10,000 users")
        print("✅ 5,000 products") 
        print("✅ 20,000 orders")
        print("✅ 50,000 order items")
        print("✅ 10,000 posts")
        print("✅ 100,000 log entries")
        print("✅ Intentionally slow queries for testing")
        print("✅ Missing indexes to demonstrate optimization")
        print("\nYou can now run:")
        print("  python p3cli.py --monitor")
        print("  python p3cli.py --analyze-queries")
        print("  python p3cli.py --ask 'Why is my query slow?'")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
    finally:
        setup.close()

if __name__ == "__main__":
    main()
