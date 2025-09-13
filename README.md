# AI-Powered MySQL Observability CLI

A powerful command-line tool that provides AI-driven database performance analysis and optimization recommendations using Google Gemini Pro. This tool analyzes MySQL queries, identifies performance bottlenecks, and provides actionable insights to improve database performance.

## 🚀 Features

### Core Functionality
- **Real-time MySQL Metrics Collection**: Monitors key performance indicators
- **AI-Powered Query Analysis**: Uses Google Gemini Pro for intelligent query analysis
- **Anomaly Detection**: ML-based detection of unusual database patterns
- **Context-Aware AI Assistant**: Ask natural language questions about your database performance
- **Comprehensive Performance Reports**: Detailed analysis with specific recommendations
- **Database Selection**: Choose which database to work with from your available MySQL databases

### AI Capabilities
- **Smart Query Analysis**: Identifies slow queries and their root causes
- **Index Recommendations**: Suggests specific indexes to create
- **Query Optimization**: Provides rewritten queries for better performance
- **Performance Insights**: Explains why queries are slow and how to fix them
- **Conversational Interface**: Ask questions like "why is query 3 slow?" or "how to fix this error?"

## 📋 Prerequisites

- Python 3.7+
- MySQL Server (installation guide below)
- Google Gemini Pro API key (free to get)
- Terminal/Command Line access

## 🏁 Quick Start for Complete Beginners

**New to MySQL?** Follow these steps in order:

1. [Install MySQL Server](#-step-1-install--start-mysql-server)
2. [Install Python Dependencies](#step-2-install-python-dependencies)
3. [Get Gemini API Key](#step-3-get-gemini-pro-api-key)
4. [Configure the Tool](#step-4-configure-the-tool)
5. [Connect to MySQL](#step-5-connect-to-mysql)
6. [Start Analyzing](#step-6-start-analyzing)

---

## 🛠️ Complete Installation Guide

### 🗄️ Step 1: Install & Start MySQL Server

#### Option A: Install MySQL (if not installed)

**macOS - Using Homebrew (Recommended):**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install MySQL
brew install mysql

# Start MySQL service
brew services start mysql

# Secure your MySQL installation (set root password)
mysql_secure_installation
```

**macOS - Using Official MySQL Installer:**
1. Download MySQL from [mysql.com/downloads/mysql](https://dev.mysql.com/downloads/mysql/)
2. Install the .dmg file
3. Start MySQL via System Preferences → MySQL → Start MySQL Server
4. Or start via command line:
```bash
sudo /usr/local/mysql/support-files/mysql.server start
```

#### Option B: Start MySQL (if already installed)

```bash
# Method 1: Using Homebrew
brew services start mysql

# Method 2: Using MySQL installer
sudo /usr/local/mysql/support-files/mysql.server start

# Method 3: Using System Preferences
# Go to System Preferences → MySQL → Start MySQL Server

# Method 4: Using launchctl (if configured)
sudo launchctl load -w /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist
```

#### Verify MySQL is Running

```bash
# Check if MySQL is running
brew services list | grep mysql
# Should show: mysql started

# Or check processes
ps aux | grep mysql

# Test connection
mysql -u root -p
# Enter your MySQL root password when prompted
```

#### Set Up MySQL User (First Time Setup)

```bash
# Connect to MySQL as root
mysql -u root -p

# Create a new user for the application (optional but recommended)
CREATE USER 'dbanalyzer'@'localhost' IDENTIFIED BY 'secure_password_123';
GRANT ALL PRIVILEGES ON *.* TO 'dbanalyzer'@'localhost';
FLUSH PRIVILEGES;

# Exit MySQL
EXIT;
```

### Step 2: Clone the Repository
```bash
git clone https://github.com/your-repo/ai-mysql-observability.git
cd ai-mysql-observability
```

### Step 3: Install Python Dependencies
```bash
# Make sure you have Python 3.7+
python3 --version

# Install dependencies
pip3 install -r requirements.txt

# If you get permission errors, try:
pip3 install --user -r requirements.txt
```

### Step 4: Get Gemini Pro API Key (FREE)

**The AI features require a free Google Gemini API key:**

1. **Visit Google AI Studio:**
   - Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account (any Gmail account works)

2. **Create API Key:**
   - Click "Create API Key"
   - Choose "Create API key in new project" (or select existing project)
   - Click "Create API Key"

3. **Copy Your Key:**
   - Copy the generated API key (starts with `AIza...`)
   - **Keep it secure** - don't share it publicly
   - You'll paste this in the next step

**Note:** Gemini API has a generous free tier that's perfect for this tool!

### Step 5: Configure the Tool

**📁 IMPORTANT: Make sure you're in the project folder!**

The `config.json` file must be in the **same folder** as `p3cli.py`.

**Find your project folder:**
```bash
# If you cloned from git:
cd ai-mysql-observability

# If you downloaded/have the project in a different folder:
cd /path/to/your/project/folder  # e.g., cd ~/Desktop/e6

# Verify you're in the right place - you should see these files:
ls -la
# Should show: p3cli.py, config.template.json, requirements.txt, etc.
```

**Copy the configuration template:**
```bash
# Copy the template (this creates config.json in the same folder)
cp config.template.json config.json
```

**Edit the configuration:**
```bash
# Option 1: Use nano (built into macOS)
nano config.json

# Option 2: Use VS Code (if installed)
code config.json

# Option 3: Use any text editor
open -a TextEdit config.json
```

**📝 EDIT THE FILE `config.json` AND ADD YOUR KEYS:**

**File to edit:** `config.json` (in the same folder as `p3cli.py`)

**What to change:**

1. **🔑 Add your Gemini API Key** on line with `"api_key"`:
   ```json
   "api_key": "AIza...your_actual_gemini_key_here"
   ```

2. **🔐 Add your MySQL password** on line with `"password"`:
   ```json
   "password": "your_actual_mysql_password"
   ```

**Complete `config.json` should look like:**

```json
{
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "MySecretPassword123"        ⬅️ YOUR MySQL password here
  },
  "gemini": {
    "api_key": "AIza-SyCbxxxxxxxxxxxxxxxxxxxxxxxx",  ⬅️ YOUR Gemini API key here
    "model": "gemini-1.5-flash",
    "enabled": true
  },
  "ml": {
    "contamination": 0.2,
    "random_state": 42,
    "min_samples_for_training": 10
  },
  "metrics": {
    "enabled": [
      "Questions",
      "Threads_connected",
      "Threads_running",
      "Slow_queries",
      "Innodb_buffer_pool_size",
      "Innodb_buffer_pool_pages_data",
      "Innodb_buffer_pool_pages_free",
      "Connections",
      "Uptime"
    ]
  }
}
```

**✅ VERIFICATION CHECKLIST:**

Before proceeding, make sure:

- [ ] You're in the project folder (same folder as `p3cli.py`)
- [ ] File `config.json` exists (copied from `config.template.json`)
- [ ] Your **Gemini API key** is in `config.json` (starts with `AIza`)
- [ ] Your **MySQL password** is in `config.json`
- [ ] Both keys are inside the quote marks `"your_key_here"`

**🔍 Quick Check:**
```bash
# Verify config.json exists and contains your keys
cat config.json | grep "api_key"
# Should show: "api_key": "AIza...your_actual_key",

cat config.json | grep "password"
# Should show: "password": "your_actual_password"
```

> 📁 **KEY LOCATION SUMMARY:**
> 
> **File:** `config.json` (same folder as `p3cli.py`)
> 
> **Two places to add keys:**
> 1. **Gemini API key** → `"api_key": "AIza...your_key"`
> 2. **MySQL password** → `"password": "your_mysql_password"`
> 
> **Folder structure:**
> ```
> your-project-folder/          # ← You should be HERE in terminal
> ├── p3cli.py                  # ← Main script
> ├── config.template.json       # ← Template (don't edit this)
> ├── config.json               # ← YOUR KEYS GO HERE!
> ├── requirements.txt
> └── README.md
> ```

### Step 6: Connect to MySQL

**Test your MySQL connection and setup:**

```bash
# Test MySQL connection (interactive setup)
python test_mysql_connection.py
```

This script will:
- Prompt you for MySQL credentials
- Test the connection
- Show available databases
- Update your `config.json` automatically
- Test some sample queries

**Example interaction:**
```
Host (default: localhost): [Press Enter]
Port (default: 3306): [Press Enter]
Username (default: root): [Press Enter or type your username]
Password: [Type your MySQL password]
```

**Test Gemini API:**
```bash
python setup_gemini.py
```

You should see:
- ✅ "Gemini Pro API key is valid!"
- A sample AI response

**If you get errors:**
- **MySQL Error:** Check if MySQL is running (`brew services start mysql`)
- **Gemini Error:** Check your API key in `config.json`
- **Module Error:** Run `pip install -r requirements.txt`

### Step 7: Select Your Database

**Choose which database to analyze:**

```bash
python p3cli.py --select-database
```

This will:
- Show all your databases (excluding system ones)
- Let you select which one to work with
- Test the connection
- Update your configuration

**Don't have any databases?** Create a test one:
```bash
python quick_setup.py
```

### Step 8: Start Analyzing!

**You're ready! Try these commands:**

```bash
# Monitor real-time metrics
python p3cli.py --monitor

# Analyze queries with AI
python p3cli.py --analyze-queries

# Ask questions about your database
python p3cli.py --ask "What's wrong with my database performance?"
python p3cli.py --ask "Which queries are the slowest?"
python p3cli.py --ask "What indexes should I create?"

# Generate comprehensive AI report
python p3cli.py --ai-analysis
```

---

## 🔧 Troubleshooting Common Issues

### 🚫 MySQL Connection Problems

**Issue:** "Error connecting to MySQL: 2003 (HY000): Can't connect to MySQL server"

**Solutions:**
```bash
# 1. Check if MySQL is running
brew services list | grep mysql
# Should show: mysql started

# 2. Start MySQL if it's stopped
brew services start mysql

# 3. Or try other methods:
sudo /usr/local/mysql/support-files/mysql.server start

# 4. Check if port 3306 is in use
lsof -i :3306
```

**Issue:** "Access denied for user 'root'@'localhost'"

**Solutions:**
```bash
# Reset MySQL root password
sudo mysql_secure_installation

# Or connect without password and set one
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
FLUSH PRIVILEGES;
EXIT;
```

### 🤖 AI/Gemini Issues

**Issue:** "Gemini analyzer not available"

**Solutions:**
1. Check your API key in `config.json`
2. Make sure `"enabled": true` in Gemini section
3. Test API key: `python setup_gemini.py`
4. Check internet connection
5. Verify API key starts with `AIza`

**Issue:** "ModuleNotFoundError: No module named 'google'"

**Solution:**
```bash
pip install google-generativeai
# or
pip install -r requirements.txt
```

### 📚 Python/Dependencies Issues

**Issue:** "ModuleNotFoundError: No module named 'mysql'"

**Solution:**
```bash
pip install mysql-connector-python
```

**Issue:** "Permission denied" when installing packages

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 🗺️ Database Issues

**Issue:** "No databases found"

**Solutions:**
1. Create a test database:
```bash
mysql -u root -p
CREATE DATABASE test_db;
USE test_db;
CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(50));
EXIT;
```

2. Or use the quick setup:
```bash
python quick_setup.py
```

**Issue:** Tool shows "Demo mode" instead of real data

**This is normal!** The tool automatically falls back to demo mode when:
- MySQL connection fails
- No real queries found
- Database is empty

---

## 👀 What to Expect

### First Run Experience

**When you run `python p3cli.py --analyze-queries` for the first time:**

✅ **With Real Database:**
```
🤖 Using AI-powered analysis with Gemini Pro...
Analyzing query 1/8...
Analyzing query 2/8...

🔴 QUERY #1 (CRITICAL)
   Execution Time: 2.80s
   Rows Examined: 4,000,000
   Rows Sent: 5,000
   Efficiency: 0.12%
   Query: SELECT u.name, COUNT(p.id)...
   
   🤖 Gemini AI Analysis:
   The query is slow because there's no index on user_id...
   
   📀 Recommended Indexes:
     • CREATE INDEX idx_users_id ON users (id);
```

✅ **Demo Mode (No MySQL):**
```
MySQL connection failed. Switching to demo mode...
🤖 Using AI-powered analysis with Gemini Pro...
[Shows analysis of synthetic slow queries for learning]
```

### AI Assistant Examples

**Ask questions after running analysis:**

```bash
# Ask about specific issues
python p3cli.py --ask "Why is query 3 slow?"

# Get optimization advice
python p3cli.py --ask "What indexes should I create first?"

# General performance questions
python p3cli.py --ask "How can I improve my database performance?"
```

**Example AI Response:**
```
🤖 AI Database Consultant
=================================================
Question: Why is query 3 slow?
-------------------------------------------------
Answer: Query 3 is slow because it's performing a full table 
scan on the 'users' table with 4M rows. The WHERE clause 
filters on 'email' but there's no index on this column.

Recommendation:
CREATE INDEX idx_users_email ON users (email);

This should reduce query time from 2.8s to under 0.01s.
=================================================
```

### Monitoring Dashboard

**When you run `python p3cli.py --monitor`:**

```
============================================================
MySQL Performance Metrics
============================================================
Metric                         Value                Status    
------------------------------------------------------------
Questions                      1000000.00           OK        
Threads_connected              45.00                OK        
Threads_running                3.00                 OK        
Slow_queries                   15.00                HIGH      
Connections                    950.00               OK        
Uptime                         86400.00             OK        
============================================================
```

---

## 🎯 Usage

### Basic Commands

#### 1. Select Your Database
```bash
python p3cli.py --select-database
```
Choose which database to work with from your available MySQL databases.

#### 2. Monitor Current Metrics
```bash
python p3cli.py --monitor
```
Displays real-time MySQL performance metrics including:
- Query throughput (Questions counter)
- Active connections
- Buffer pool usage
- Slow query count
- Uptime

#### 3. Analyze Queries with AI
```bash
python p3cli.py --analyze-queries
```
Performs comprehensive AI-powered analysis of your database queries:
- Identifies slow queries
- Explains performance bottlenecks
- Provides specific index recommendations
- Suggests query optimizations
- Generates detailed performance reports

#### 4. Ask AI Questions
```bash
python p3cli.py --ask "why is query 3 slow?"
python p3cli.py --ask "how to fix this error?"
python p3cli.py --ask "what's the worst performing query?"
```
Ask natural language questions about your database performance. The AI uses context from recent analysis to provide specific, actionable answers.

#### 5. Run AI Analysis
```bash
python p3cli.py --ai-analysis
```
Generates a comprehensive AI-powered summary report of your database performance.

#### 6. Check for Anomalies
```bash
python p3cli.py --analyze
```
Uses machine learning to detect unusual patterns in your database metrics.

### Demo Mode

If you don't have a MySQL database set up, the tool automatically falls back to demo mode with synthetic data:

```bash
python p3cli.py --analyze-queries
# Will use demo data if MySQL is not available
```

### Quick Setup (Optional)

For testing purposes, you can quickly set up a MySQL database with sample data:

```bash
python quick_setup.py
```

This creates a test database with sample tables and data for demonstration.

## 📊 Understanding the Output

### Query Analysis Results

Each query analysis includes:

- **Execution Time**: How long the query takes to run
- **Rows Examined**: Number of rows the database had to check
- **Rows Sent**: Number of rows returned to the user
- **Efficiency Ratio**: Percentage of examined rows that were actually useful
- **Severity Level**: Critical, High, Medium, or Low
- **AI Analysis**: Detailed explanation of why the query is slow
- **Recommended Indexes**: Specific CREATE INDEX statements
- **Query Optimizations**: Suggested query improvements
- **Performance Impact**: Estimated improvement after optimization

### Example Output

```
🔴 QUERY #1 (CRITICAL)
   Execution Time: 2.80s
   Rows Examined: 4,000,000
   Rows Sent: 5,000
   Efficiency: 0.12%
   Query: SELECT u.name, COUNT(p.id) as post_count FROM users u LEFT JOIN posts p ON u.id = p.user_id

   🤖 Gemini AI Analysis:
   The query is slow primarily due to a lack of appropriate indexes...

   📊 Recommended Indexes:
     • CREATE INDEX idx_users_id ON users (id);
     • CREATE INDEX idx_posts_user_id_count ON posts (user_id, id);

   📈 Expected Improvement: 96%+ performance improvement
```

## 🔧 Advanced Features

### Context-Aware AI

The AI assistant remembers your recent database analysis, so you can ask follow-up questions without providing context:

```bash
# First, run analysis
python p3cli.py --analyze-queries

# Then ask specific questions
python p3cli.py --ask "why is query 3 slow?"
python p3cli.py --ask "how to fix the JOIN performance?"
python p3cli.py --ask "what indexes should I create first?"
```

### Custom Query Analysis

You can analyze specific queries by modifying the demo queries in `query_analyzer.py` or by connecting to your real MySQL database.

### Performance Monitoring

The tool tracks historical metrics in `metrics_history.json` for trend analysis and anomaly detection.

## 📁 Project Structure

```
ai-mysql-observability/
├── p3cli.py                 # Main CLI application
├── query_analyzer.py        # Rule-based query analysis
├── gemini_analyzer.py       # AI-powered analysis with Gemini Pro
├── select_database.py       # Database selection utility
├── config.template.json     # Configuration template
├── config.json             # Your configuration (DO NOT COMMIT)
├── requirements.txt        # Python dependencies
├── setup_gemini.py         # Gemini API setup script
├── test_mysql_connection.py # MySQL connection tester
├── quick_setup.py          # Quick database setup
├── setup_mysql_fast.py     # Fast MySQL setup with sample data
├── metrics_history.json    # Historical metrics storage
├── recent_analysis.json    # Recent analysis context for AI
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## ⚙️ Configuration

### MySQL Configuration

Update the `mysql` section in `config.json`:

```json
{
  "mysql": {
    "host": "localhost",           # Your MySQL host
    "port": 3306,                  # Your MySQL port
    "user": "your_username",       # Your MySQL username
    "password": "your_password",   # Your MySQL password
    "database": "your_database"    # Your database name
  }
}
```

### Gemini Pro Configuration

Update the `gemini` section in `config.json`:

```json
{
  "gemini": {
    "api_key": "your_api_key_here",  # Your Gemini Pro API key
    "model": "gemini-1.5-flash",     # Model to use
    "enabled": true                  # Enable/disable AI features
  }
}
```

### ML Configuration

Adjust the `ml` section for anomaly detection:

```json
{
  "ml": {
    "contamination": 0.2,           # Fraction of expected outliers
    "random_state": 42,             # For reproducible results
    "min_samples_for_training": 10  # Minimum samples for model training
  }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **"Gemini analyzer not available"**
   - Check your API key in `config.json`
   - Ensure your API key is valid and has sufficient quota
   - Run `python setup_gemini.py` to test the connection

2. **"Error connecting to MySQL"**
   - Check your MySQL server is running
   - Verify connection details in `config.json`
   - Run `python test_mysql_connection.py` to test connection

3. **"No recent analysis data available"**
   - Run `python p3cli.py --analyze-queries` first to create analysis context

4. **"No databases found"**
   - Ensure your MySQL user has access to databases
   - Check if you have any user databases (not system databases)

### Demo Mode

If you encounter MySQL connection issues, the tool automatically switches to demo mode with synthetic data, so you can still test all features.

## 🔐 Security Notes

**IMPORTANT**: This tool handles sensitive information (database credentials, API keys).

- **Never commit `config.json` to git** - it's already in `.gitignore`
- **Use `config.template.json` as a reference**
- **Keep your API keys secure**
- **Use strong database passwords**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini Pro for AI capabilities
- MySQL community for database insights
- Scikit-learn for machine learning components

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the configuration in `config.json`
3. Ensure all dependencies are installed
4. Create an issue in the GitHub repository

## 🚀 Quick Start Guide

### For New Users:

1. **Clone and Install:**
   ```bash
   git clone https://github.com/yourusername/ai-mysql-observability.git
   cd ai-mysql-observability
   pip install -r requirements.txt
   ```

2. **Get API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create API key
   - Copy the key

3. **Configure:**
   ```bash
   cp config.template.json config.json
   # Edit config.json with your MySQL and Gemini details
   ```

4. **Test:**
   ```bash
   python p3cli.py --select-database
   python p3cli.py --analyze-queries
   ```

5. **Ask Questions:**
   ```bash
   python p3cli.py --ask "What's wrong with my database?"
   ```

---

**Happy Database Optimizing! 🚀**