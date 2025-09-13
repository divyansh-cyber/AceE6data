# Setup Guide for New Users

This guide will walk you through setting up the AI-Powered MySQL Observability CLI tool from scratch.

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.7 or higher installed
- [ ] MySQL Server running on your machine
- [ ] A Google account (for Gemini Pro API)
- [ ] Git installed (to clone the repository)

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/...
cd ai-mysql-observability
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

If you encounter any issues, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Get Your Gemini Pro API Key

1. **Go to Google AI Studio:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key:**
   - Click "Create API Key"
   - Choose "Create API key in new project" or select existing project
   - Copy the generated API key (starts with `AIza...`)

3. **Keep it Safe:**
   - Store the API key securely
   - You'll need it in the next step

### Step 4: Configure the Tool

1. **Copy the configuration template:**
   ```bash
   cp config.template.json config.json
   ```

2. **Edit the configuration file:**
   ```bash
   nano config.json
   # or use your preferred editor (VS Code, Sublime, etc.)
   ```

3. **Update the following sections:**

   **MySQL Configuration:**
   ```json
   {
     "mysql": {
       "host": "localhost",
       "port": 3306,
       "user": "your_mysql_username",
       "password": "your_mysql_password",
     }
   }
   ```

   **Gemini Pro Configuration:**
   ```json
   {
     "gemini": {
       "api_key": "your-key",
       "model": "gemini-1.5-flash",
       "enabled": true
     }
   }
   ```

### Step 5: Test Your Setup

1. **Test MySQL Connection:**
   ```bash
   python test_mysql_connection.py
   ```
   - This will verify your MySQL credentials
   - If successful, you'll see "✅ Connection successful!"

2. **Test Gemini API:**
   ```bash
   python setup_gemini.py
   ```
   - This will verify your API key
   - If successful, you'll see "✅ Gemini Pro API key is valid!"

### Step 6: Select Your Database

```bash
python p3cli.py --select-database
```

This will:
- Show all available databases
- Let you choose which one to work with
- Test the connection
- Update your configuration

### Step 7: Run Your First Analysis

```bash
# Monitor your database
python p3cli.py --monitor

# Analyze queries
python p3cli.py --analyze-queries

# Ask AI questions
python p3cli.py --ask "What tables are in this database?"
```

## 🔧 Troubleshooting Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'mysql'"

**Solution:**
```bash
pip install mysql-connector-python
```

### Issue 2: "Error connecting to MySQL: 2003 (HY000): Can't connect to MySQL server"

**Solutions:**
- Check if MySQL is running: `sudo service mysql start` (Linux) or `brew services start mysql` (Mac)
- Verify your credentials in `config.json`
- Check if the port is correct (default is 3306)

### Issue 3: "Gemini analyzer not available"

**Solutions:**
- Check your API key in `config.json`
- Ensure the API key is valid
- Check your internet connection

### Issue 4: "No databases found"

**Solutions:**
- Make sure you have user databases (not just system databases)
- Check if your MySQL user has proper permissions
- Create a test database if needed

## 🎯 What to Expect

### First Run
When you run `python p3cli.py --analyze-queries` for the first time, you might see:
- Demo data if no real queries are found
- AI analysis of your database structure
- Performance recommendations

### AI Features
The AI can help you with:
- Identifying slow queries
- Suggesting indexes
- Explaining performance issues
- Optimizing queries

### Example Questions to Ask
```bash
python p3cli.py --ask "Why is my database slow?"
python p3cli.py --ask "What indexes should I create?"
python p3cli.py --ask "Which queries are taking the most time?"
```

## 📚 Next Steps

1. **Explore the Features:**
   - Try different commands
   - Ask various questions
   - Monitor your database performance

2. **Customize:**
   - Adjust ML parameters in `config.json`
   - Add custom metrics
   - Modify query analysis rules

3. **Integrate:**
   - Add to your monitoring workflow
   - Set up regular analysis
   - Use in your development process

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide first**
2. **Review the main README.md**
3. **Check the troubleshooting section**
4. **Create an issue on GitHub**

## ✅ Success Checklist

You've successfully set up the tool when you can:

- [ ] Run `python p3cli.py --monitor` without errors
- [ ] Run `python p3cli.py --analyze-queries` and see analysis
- [ ] Run `python p3cli.py --ask "test question"` and get AI response
- [ ] See your database in the selection menu

---

**Congratulations! You're ready to optimize your MySQL database with AI! 🎉**
