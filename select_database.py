#!/usr/bin/env python3
"""
Database Selection Script for AI-Powered MySQL Observability CLI
This script helps you select which database to work with.
"""

import json
import mysql.connector
from typing import List, Dict

def get_available_databases(host: str, port: int, user: str, password: str) -> List[str]:
    """Get list of available databases from MySQL server."""
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        
        # Filter out system databases
        system_dbs = {'information_schema', 'performance_schema', 'mysql', 'sys'}
        user_databases = [db for db in databases if db not in system_dbs]
        
        cursor.close()
        connection.close()
        
        return user_databases
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return []

def display_databases(databases: List[str]) -> None:
    """Display available databases in a nice format."""
    if not databases:
        print("❌ No user databases found!")
        return
    
    print("\n📊 Available Databases:")
    print("=" * 40)
    for i, db in enumerate(databases, 1):
        print(f"{i:2d}. {db}")
    print("=" * 40)

def select_database(databases: List[str]) -> str:
    """Let user select a database."""
    while True:
        try:
            choice = input(f"\nSelect database (1-{len(databases)}): ").strip()
            if not choice:
                print("Please enter a number.")
                continue
                
            index = int(choice) - 1
            if 0 <= index < len(databases):
                return databases[index]
            else:
                print(f"Please enter a number between 1 and {len(databases)}")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None

def update_config(database: str) -> None:
    """Update config.json with selected database."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        config['mysql']['database'] = database
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Updated config.json to use database: {database}")
    except Exception as e:
        print(f"Error updating config: {e}")

def test_database_connection(database: str, host: str, port: int, user: str, password: str) -> bool:
    """Test connection to selected database."""
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s", (database,))
        table_count = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        print(f"✅ Successfully connected to '{database}'")
        print(f"📊 Found {table_count} tables in the database")
        return True
    except Exception as e:
        print(f"❌ Error connecting to database '{database}': {e}")
        return False

def main():
    """Main function."""
    print("🗄️  Database Selection for AI-Powered MySQL Observability CLI")
    print("=" * 65)
    
    # Load current config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found! Please run setup first.")
        return
    
    mysql_config = config['mysql']
    host = mysql_config['host']
    port = mysql_config['port']
    user = mysql_config['user']
    password = mysql_config['password']
    current_db = mysql_config.get('database', '')
    
    print(f"🔗 Connecting to MySQL server: {host}:{port}")
    print(f"👤 User: {user}")
    if current_db:
        print(f"📊 Current database: {current_db}")
    
    # Get available databases
    print("\n🔍 Fetching available databases...")
    databases = get_available_databases(host, port, user, password)
    
    if not databases:
        print("❌ No databases found or connection failed.")
        return
    
    # Display databases
    display_databases(databases)
    
    # Let user select
    selected_db = select_database(databases)
    if not selected_db:
        return
    
    # Test connection
    print(f"\n🧪 Testing connection to '{selected_db}'...")
    if test_database_connection(selected_db, host, port, user, password):
        # Update config
        update_config(selected_db)
        
        print(f"\n🎉 Ready to use '{selected_db}' with the CLI tool!")
        print("\nNext steps:")
        print("1. Run: python p3cli.py --monitor")
        print("2. Run: python p3cli.py --analyze-queries")
        print("3. Run: python p3cli.py --ask 'What tables are in this database?'")
    else:
        print("❌ Failed to connect to selected database.")

if __name__ == "__main__":
    main()
