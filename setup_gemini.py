#!/usr/bin/env python3
"""
Gemini Pro Setup Script

This script helps you set up Gemini Pro API integration for the MySQL observability tool.
"""

import json
import os

def setup_gemini():
    """Set up Gemini Pro API configuration."""
    print("🚀 Gemini Pro Setup for MySQL Observability Tool")
    print("="*60)
    
    # Get API key
    print("\n1. Get your Gemini Pro API key:")
    print("   • Go to: https://makersuite.google.com/app/apikey")
    print("   • Sign in with your Google account")
    print("   • Click 'Create API Key'")
    print("   • Copy the generated API key")
    
    api_key = input("\n2. Enter your Gemini Pro API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Load current config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found. Please run the main setup first.")
        return
    
    # Update config
    if 'gemini' not in config:
        config['gemini'] = {}
    
    config['gemini']['api_key'] = api_key
    config['gemini']['model'] = 'gemini-pro'
    config['gemini']['enabled'] = True
    
    # Save config
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Gemini Pro configuration updated!")
    
    # Test the connection
    print("\n3. Testing Gemini Pro connection...")
    try:
        from gemini_analyzer import GeminiAnalyzer
        analyzer = GeminiAnalyzer(api_key=api_key)
        print("✅ Gemini Pro connection successful!")
        
        # Test with a simple question
        print("\n4. Testing AI analysis...")
        test_question = "What is a database index?"
        answer = analyzer.ask_question(test_question)
        print(f"🤖 Test Question: {test_question}")
        print(f"🤖 Answer: {answer[:100]}...")
        print("✅ AI analysis working!")
        
    except Exception as e:
        print(f"❌ Error testing Gemini Pro: {e}")
        print("Please check your API key and try again.")
        return
    
    print("\n" + "="*60)
    print("🎉 GEMINI PRO SETUP COMPLETE!")
    print("="*60)
    print("Your MySQL observability tool now supports:")
    print("✅ Gemini Pro AI analysis")
    print("✅ Natural language query explanations")
    print("✅ Advanced performance recommendations")
    print("✅ Conversational database consulting")
    print("\nYou can now run:")
    print("  python p3cli.py --ask 'Why is my query slow?'")
    print("  python p3cli.py --analyze-queries")
    print("  python p3cli.py --ai-analysis")

if __name__ == "__main__":
    setup_gemini()
