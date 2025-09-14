# 🚀 AI-Powered MySQL Observability CLI Tool

A command-line tool to collect MySQL metrics, monitor performance, and detect anomalies using machine learning.

---

## 📦 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/<your-username>/mysql-observability-cli.git
   cd mysql-observability-cli
Set up a Python environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
Install dependencies
pip install -r requirements.txt
🛠️ Configuration
Start your MySQL server
Make sure MySQL is running locally (or on a host you can connect to).
Edit config.json
On first run, the tool will auto-create config.json.
Update it with your credentials:
{
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "user": "youruser",
    "password": "yourpassword",
    "database": "mysql"
  },
  "ml": {
    "contamination": 0.1,
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
▶️ Usage
1. Select a database (optional helper script)
If you have select_database.py (optional helper):
python select_database.py
This lets you choose which MySQL database to monitor.
2. Collect metrics (--monitor)
python p3cli.py --monitor
Collects 100 samples of MySQL metrics (default in your code).
Saves them in metrics_history.json.
Displays the last one in a formatted table.
3. Run anomaly detection (--analyze)
python p3cli.py --analyze
Trains an IsolationForest ML model on historical metrics.
Detects if the most recent datapoint looks anomalous.
Needs at least 10 datapoints (already satisfied if you ran --monitor once with 100 samples).
4. Advanced analysis
AI-based anomaly detection
python p3cli.py --ai-analyze
Uses a stricter AI model (IsolationForest + preprocessing).
Query analysis
python p3cli.py --analyze-queries
Collects recent SQL queries (from performance schema) and flags slow or anomalous ones.
5. Show current configuration
python p3cli.py --config
📊 Example Workflow
# Step 1: Start MySQL server
brew services start mysql   # macOS
sudo systemctl start mysql  # Linux

# Step 2: Run monitor (collects 100 datapoints)
python p3cli.py --monitor

# Step 3: Run anomaly detection
python p3cli.py --analyze

# Step 4 (optional): Run AI-enhanced anomaly detection
python p3cli.py --ai-analyze
🗂️ Project Structure
.
├── p3cli.py              # Main CLI tool
├── config.json           # User configuration (auto-created on first run)
├── metrics_history.json  # Saved metrics history
├── recent_analysis.json  # Last analysis results
├── select_database.py    # (Optional) script to pick DB interactively
├── requirements.txt      # Dependencies
└── README.md             # This guide
⚠️ Notes
metrics_history.json and recent_analysis.json should not be version-controlled (add them to .gitignore).
You need at least 10 datapoints for anomaly detection (already covered since --monitor collects 100 at once).
If MySQL is not running, the tool falls back to demo mode (random simulated metrics).
