# AI-Powered MySQL Observability CLI

A command-line tool for real-time MySQL performance monitoring and AI-powered query optimization using Google Gemini Pro.

## Key Features

* **Live Metrics Monitoring** – Tracks key MySQL performance indicators
* **AI Query Analysis** – Identifies slow queries, bottlenecks, and suggests fixes
* **Index Recommendations** – Proposes optimal indexes to improve performance
* **Anomaly Detection** – Uses ML to detect unusual database patterns
* **Context-Aware Assistant** – Ask natural language questions about performance

## Prerequisites

* Python 3.7+
* MySQL Server (running locally or remotely)
* Google Gemini API key

## Quick Start

1. **Clone and Install**

   ```bash
   git clone https://github.com/yourusername/ai-mysql-observability.git
   cd ai-mysql-observability
   pip install -r requirements.txt
   ```

2. **Configure**
   Copy the template and add credentials:

   ```bash
   cp config.template.json config.json
   ```

   Edit `config.json` with:

   * Your MySQL username, password, and database
   * Your Gemini API key

3. **Test Connection**

   ```bash
   python test_mysql_connection.py
   ```

4. **Run the Tool**

   ```bash
   python p3cli.py --monitor          # Monitor metrics
   python p3cli.py --analyze-queries  # AI query analysis
   python p3cli.py --ask "Top slow queries?"
   ```

## Troubleshooting

* **MySQL Error**: Verify server is running and credentials are correct.
* **Gemini Error**: Check API key in `config.json` and test with `python setup_gemini.py`.
* **Missing Modules**: Run `pip install -r requirements.txt`.

## Security Notes

* Keep `config.json` private (never commit to version control).
* Use strong database passwords and secure your API keys.

**Happy Database Optimizing! **
