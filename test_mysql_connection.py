#!/usr/bin/env python3
"""
MySQL Connection Test Script

This script tests your MySQL connection and shows what data is available.
"""

import mysql.connector
import json
from datetime import datetime

def test_mysql_connection():
    """Test MySQL connection and show database info."""
    print("🔍 Testing MySQL Connection")
    print("="*50)
    
    # Get connection details
    print("Enter your MySQL connection details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = int(input("Port (default: 3306): ").strip() or "3306")
    user = input("Username (default: root): ").strip() or "root"
    password = input("Password: ").strip()
    
    try:
        # Test connection
        print("\n🔄 Connecting to MySQL...")
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        print("✅ Connected to MySQL successfully!")
        
        cursor = connection.cursor()
        
        # Show MySQL version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"📊 MySQL Version: {version}")
        
        # Show databases
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        print(f"📊 Available databases: {', '.join(databases)}")
        
        # Check if observability_test exists
        if 'observability_test' in databases:
            print("✅ observability_test database found!")
            
            # Switch to the database
            cursor.execute("USE observability_test")
            
            # Show tables
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📊 Tables: {', '.join(tables)}")
            
            # Show table sizes
            print("\n📊 Table sizes:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,} rows")
            
            # Test some queries
            print("\n🔍 Testing some queries:")
            
            # Test a simple query
            cursor.execute("SELECT COUNT(*) FROM users WHERE city = 'New York'")
            ny_users = cursor.fetchone()[0]
            print(f"  Users in New York: {ny_users:,}")
            
            # Test a slow query (missing index)
            start_time = datetime.now()
            cursor.execute("SELECT * FROM users WHERE age BETWEEN 25 AND 35 AND city = 'Los Angeles' LIMIT 10")
            results = cursor.fetchall()
            end_time = datetime.now()
            query_time = (end_time - start_time).total_seconds()
            print(f"  Query time for age/city filter: {query_time:.3f}s")
            
            # Test another slow query
            start_time = datetime.now()
            cursor.execute("SELECT * FROM products WHERE name LIKE '%laptop%' LIMIT 10")
            results = cursor.fetchall()
            end_time = datetime.now()
            query_time = (end_time - start_time).total_seconds()
            print(f"  Query time for product search: {query_time:.3f}s")
            
        else:
            print("⚠️ observability_test database not found.")
            print("Run: python setup_mysql_database.py to create it.")
        
        # Update config
        print("\n🔄 Updating config.json...")
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            config['mysql']['host'] = host
            config['mysql']['port'] = port
            config['mysql']['user'] = user
            config['mysql']['password'] = password
            config['mysql']['database'] = 'observability_test' if 'observability_test' in databases else 'mysql'
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ Updated config.json with your MySQL settings")
            
        except Exception as e:
            print(f"❌ Error updating config: {e}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*50)
        print("🎉 MySQL Connection Test Complete!")
        print("="*50)
        print("You can now run:")
        print("  python p3cli.py --monitor")
        print("  python p3cli.py --analyze-queries")
        print("  python p3cli.py --ask 'Why is my query slow?'")
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL is running")
        print("2. Check your username and password")
        print("3. Verify the host and port are correct")
        print("4. Ensure the user has necessary privileges")

if __name__ == "__main__":
    test_mysql_connection()
