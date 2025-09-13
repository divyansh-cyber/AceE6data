#!/usr/bin/env python3
"""
Quick Setup Script for MySQL Observability Tool

This script helps you quickly set up everything:
1. Install dependencies
2. Set up MySQL database with test data
3. Configure the tool
4. Test the integration
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and show progress."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Quick Setup for MySQL Observability Tool")
    print("="*60)
    
    # Step 1: Install dependencies
    print("\n1️⃣ Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        return
    
    # Step 2: Check MySQL connection
    print("\n2️⃣ Checking MySQL connection...")
    print("Please make sure MySQL is running and you have the connection details ready.")
    
    # Step 3: Run database setup
    print("\n3️⃣ Setting up MySQL database...")
    print("This will create a test database with millions of rows and slow queries.")
    
    response = input("Do you want to proceed with database setup? (y/n): ").strip().lower()
    if response == 'y':
        if not run_command("python setup_mysql_database.py", "Database setup"):
            print("❌ Database setup failed. Please check your MySQL connection.")
            return
    else:
        print("⏭️ Skipping database setup. You can run it later with: python setup_mysql_database.py")
    
    # Step 4: Test the tool
    print("\n4️⃣ Testing the tool...")
    
    # Test basic functionality
    if run_command("python p3cli.py --config", "Testing basic configuration"):
        print("✅ Basic tool functionality working")
    
    # Test query analysis
    if run_command("python p3cli.py --analyze-queries", "Testing query analysis"):
        print("✅ Query analysis working")
    
    # Test OpenAI integration (if configured)
    if run_command("python p3cli.py --ask 'What is MySQL?'", "Testing OpenAI integration"):
        print("✅ OpenAI integration working")
    else:
        print("⚠️ OpenAI integration not configured. Run: python setup_openai.py")
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("Your MySQL observability tool is ready!")
    print("\nAvailable commands:")
    print("  python p3cli.py --monitor              # Basic metrics")
    print("  python p3cli.py --analyze              # Anomaly detection")
    print("  python p3cli.py --analyze-queries      # Query analysis")
    print("  python p3cli.py --ask 'question'       # Ask AI (if configured)")
    print("  python p3cli.py --ai-analysis          # AI analysis (if configured)")
    print("\nFor OpenAI setup: python setup_openai.py")
    print("For database setup: python setup_mysql_database.py")

if __name__ == "__main__":
    main()
