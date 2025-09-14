#!/usr/bin/env python3
"""
AI-Powered MySQL Observability CLI Tool

This tool provides observability for MySQL databases by:
1. Collecting key performance metrics
2. Using ML-based anomaly detection
3. Providing CLI interface for monitoring and analysis

Usage:
    python p3cli.py --monitor    # Collect and display current metrics
    python p3cli.py --analyze    # Run anomaly detection
    python p3cli.py --config     # Show current configuration
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import mysql.connector
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from query_analyzer import QueryAnalyzer
from gemini_analyzer import GeminiAnalyzer


class MySQLObservabilityTool:
    """Main class for MySQL observability operations."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize the tool with configuration."""
        self.config = self._load_config(config_file)
        self.model = None
        self.scaler = StandardScaler()
        self.metrics_history = []
        self.query_analyzer = QueryAnalyzer()
        self.gemini_analyzer = None
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file or create default."""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            default_config = {
                "mysql": {
                    "host": "localhost",
                    "port": 3306,
                    "user": "root",
                    "password": "",
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
                },
                "gemini": {
                    "api_key": "",
                    "model": "gemini-1.5-flash",
                    "enabled": False
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default configuration file: {config_file}")
            return default_config
    
    def connect_to_mysql(self) -> Optional[mysql.connector.connection.MySQLConnection]:
        """Establish connection to MySQL database."""
        try:
            connection = mysql.connector.connect(
                host=self.config["mysql"]["host"],
                port=self.config["mysql"]["port"],
                user=self.config["mysql"]["user"],
                password=self.config["mysql"]["password"],
                database=self.config["mysql"]["database"]
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def collect_metrics(self, demo_mode: bool = False) -> Dict[str, float]:
        """Collect MySQL performance metrics."""
        if demo_mode:
            return self._generate_demo_metrics()
        
        connection = self.connect_to_mysql()
        if not connection:
            return {}
        
        metrics = {}
        cursor = connection.cursor()
        
        try:
            for metric_name in self.config["metrics"]["enabled"]:
                try:
                    cursor.execute(f"SHOW GLOBAL STATUS LIKE '{metric_name}';")
                    result = cursor.fetchone()
                    if result:
                        metrics[metric_name] = float(result[1]) if result[1].isdigit() else 0.0
                    else:
                        metrics[metric_name] = 0.0
                except Exception as e:
                    print(f"Warning: Could not collect metric {metric_name}: {e}")
                    metrics[metric_name] = 0.0
            
            metrics['timestamp'] = datetime.now().timestamp()
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
        finally:
            cursor.close()
            connection.close()
        
        return metrics
    
    def _generate_demo_metrics(self) -> Dict[str, float]:
        """Generate demo metrics for testing when MySQL is not available."""
        import random
        
        base_metrics = {
            'Questions': 1000000,
            'Threads_connected': 50,
            'Threads_running': 5,
            'Slow_queries': 10,
            'Innodb_buffer_pool_size': 134217728,
            'Innodb_buffer_pool_pages_data': 8000,
            'Innodb_buffer_pool_pages_free': 1000,
            'Connections': 1000,
            'Uptime': 86400
        }
        
        metrics = {}
        for metric, base_value in base_metrics.items():
            variation = random.uniform(-0.1, 0.1)
            metrics[metric] = max(0, base_value * (1 + variation))
        
        metrics['timestamp'] = datetime.now().timestamp()
        return metrics
    
    def display_metrics(self, metrics: Dict[str, float]) -> None:
        """Display metrics in a formatted table."""
        if not metrics:
            print("No metrics collected.")
            return
        
        print("\n" + "="*60)
        print("MySQL Performance Metrics")
        print("="*60)
        print(f"{'Metric':<30} {'Value':<20} {'Status':<10}")
        print("-"*60)
        
        thresholds = {
            'Threads_connected': 100,
            'Threads_running': 50,
            'Slow_queries': 10,
            'Questions': 1000000
        }
        
        for metric, value in metrics.items():
            if metric == 'timestamp':
                continue
                
            status = "OK"
            if metric in thresholds:
                if value > thresholds[metric]:
                    status = "HIGH"
                elif value < 0:
                    status = "ERROR"
            
            print(f"{metric:<30} {value:<20.2f} {status:<10}")
        
        print("="*60)
    
    def train_anomaly_model(self, metrics_data: List[Dict[str, float]]) -> None:
        """Train the anomaly detection model."""
        if len(metrics_data) < self.config["ml"]["min_samples_for_training"]:
            print(f"Not enough data for training. Need at least {self.config['ml']['min_samples_for_training']} samples.")
            return
        
        df = pd.DataFrame(metrics_data)
        numeric_columns = [col for col in df.columns if col != 'timestamp']
        X = df[numeric_columns].values
        
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = IsolationForest(
            contamination=self.config["ml"]["contamination"],
            random_state=self.config["ml"]["random_state"]
        )
        self.model.fit(X_scaled)
        
        print(f"Anomaly detection model trained on {len(metrics_data)} samples.")
    
    def detect_anomalies(self, current_metrics: Dict[str, float]) -> Tuple[bool, float]:
        """Detect anomalies in current metrics."""
        if self.model is None:
            print("Model not trained yet. Collecting more data...")
            return False, 0.0
        
        numeric_columns = [col for col in current_metrics.keys() if col != 'timestamp']
        current_values = [current_metrics[col] for col in numeric_columns]
        X_current = np.array(current_values).reshape(1, -1)
        
        X_current_scaled = self.scaler.transform(X_current)
        
        prediction = self.model.predict(X_current_scaled)[0]
        anomaly_score = self.model.decision_function(X_current_scaled)[0]
        
        is_anomaly = prediction == -1
        return is_anomaly, anomaly_score
    
    def save_metrics(self, metrics: Dict[str, float]) -> None:
        """Save metrics to history file."""
        self.metrics_history.append(metrics)
        
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
        
        with open('metrics_history.json', 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
    
    def load_metrics_history(self) -> List[Dict[str, float]]:
        """Load metrics history from file."""
        if os.path.exists('metrics_history.json'):
            with open('metrics_history.json', 'r') as f:
                return json.load(f)
        return []
    
    def show_config(self) -> None:
        """Display current configuration."""
        print("\n" + "="*50)
        print("Current Configuration")
        print("="*50)
        print(f"MySQL Host: {self.config['mysql']['host']}:{self.config['mysql']['port']}")
        print(f"MySQL User: {self.config['mysql']['user']}")
        print(f"Database: {self.config['mysql']['database']}")
        print(f"ML Contamination: {self.config['ml']['contamination']}")
        print(f"Enabled Metrics: {', '.join(self.config['metrics']['enabled'])}")
        print("="*50)
    
    
    def _get_gemini_analyzer(self) -> Optional[GeminiAnalyzer]:
        """Get Gemini analyzer instance, initializing if needed."""
        if not self.config.get("gemini", {}).get("enabled", False):
            return None
        
        if self.gemini_analyzer is None:
            try:
                api_key = self.config.get("gemini", {}).get("api_key") or os.getenv('GEMINI_API_KEY')
                if not api_key:
                    print("⚠️  Gemini API key not found. Set GEMINI_API_KEY environment variable or update config.json")
                    return None
                
                self.gemini_analyzer = GeminiAnalyzer(api_key=api_key)
                print("✅ Gemini analyzer initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Gemini analyzer: {e}")
                return None
        
        return self.gemini_analyzer
    
    def analyze_queries(self) -> None:
        """Analyze slow queries and provide detailed recommendations."""
        print("\n" + "="*80)
        print("DETAILED QUERY ANALYSIS & RECOMMENDATIONS")
        print("="*80)
        
        demo_queries = self.query_analyzer.get_demo_queries(8)
        
        print(f"Analyzing {len(demo_queries)} queries...\n")
        
        gemini_analyzer = self._get_gemini_analyzer()
        
        if gemini_analyzer:
            print("🤖 Using AI-powered analysis with Gemini Pro...")
            analyses = gemini_analyzer.analyze_multiple_queries(demo_queries)
            self._display_gemini_analyses(analyses)
        else:
            print("❌ Gemini Pro is not available. Please check your API key.")
            print("Run: python setup_gemini.py")
            return
        
        summary = {
            'total_queries': len(analyses),
            'slow_queries': sum(1 for a in analyses if a.get('execution_time', 0) > 2.0),
            'critical_queries': sum(1 for a in analyses if a.get('severity') == 'critical'),
            'high_priority_queries': sum(1 for a in analyses if a.get('severity') == 'high'),
            'avg_execution_time': sum(a.get('execution_time', 0) for a in analyses) / len(analyses),
            'total_rows_examined': sum(a.get('rows_examined', 0) for a in analyses),
            'total_rows_sent': sum(a.get('rows_sent', 0) for a in analyses),
            'issue_counts': {}
        }
        summary['slow_query_percentage'] = (summary['slow_queries'] / summary['total_queries']) * 100
        self._display_query_summary(summary)
    
    
    def _display_gemini_analyses(self, analyses: List[Dict]) -> None:
        """Display Gemini-powered query analyses."""
        for i, analysis in enumerate(analyses, 1):
            severity_icon = {
                'critical': '🔴',
                'high': '🟠', 
                'medium': '🟡',
                'low': '🟢'
            }.get(analysis['severity'], '⚪')
            
            print(f"{severity_icon} QUERY #{i} ({analysis['severity'].upper()})")
            print(f"   Execution Time: {analysis['execution_time']:.2f}s")
            print(f"   Rows Examined: {analysis['rows_examined']:,}")
            print(f"   Rows Sent: {analysis['rows_sent']:,}")
            print(f"   Efficiency: {analysis.get('efficiency_ratio', 0):.2%}")
            print(f"   Query: {analysis['query'][:80]}{'...' if len(analysis['query']) > 80 else ''}")
            
            print(f"\n   🤖 Gemini AI Analysis:")
            print(f"   {analysis['ai_analysis']}")
            
            if analysis.get('indexes'):
                print(f"\n   📊 Recommended Indexes:")
                for idx in analysis['indexes'][:3]:
                    print(f"     • {idx}")
            
            if analysis.get('estimated_improvement'):
                print(f"\n   📈 Expected Improvement: {analysis['estimated_improvement']}")
            
            print("-" * 80)
    
    
    def _display_query_summary(self, summary: Dict) -> None:
        """Display query analysis summary."""
        print("\n" + "="*60)
        print("QUERY PERFORMANCE SUMMARY")
        print("="*60)
        print(f"Total Queries Analyzed: {summary['total_queries']}")
        print(f"Slow Queries: {summary['slow_queries']} ({summary['slow_query_percentage']:.1f}%)")
        print(f"Critical Issues: {summary['critical_queries']}")
        print(f"High Priority Issues: {summary['high_priority_queries']}")
        print(f"Average Execution Time: {summary['avg_execution_time']:.2f}s")
        print(f"Total Rows Examined: {summary['total_rows_examined']:,}")
        print(f"Total Rows Sent: {summary['total_rows_sent']:,}")
        
        if summary['issue_counts']:
            print("\nIssue Breakdown:")
            for issue, count in summary['issue_counts'].items():
                print(f"  • {issue.replace('_', ' ').title()}: {count}")
        
        print("="*60)
    
    def generate_query_report(self) -> None:
        """Generate a comprehensive query performance report."""
        print("\n" + "="*80)
        print("COMPREHENSIVE QUERY PERFORMANCE REPORT")
        print("="*80)
        
        all_queries = self.query_analyzer.get_demo_queries(10)
        analyses = [self.query_analyzer.analyze_query_performance(q) for q in all_queries]
        
        analyses.sort(key=lambda x: (x['severity'] == 'critical', x['execution_time']), reverse=True)
        
        print("🚨 CRITICAL ISSUES (Immediate Action Required):")
        critical_queries = [a for a in analyses if a['severity'] == 'critical']
        if critical_queries:
            for analysis in critical_queries:
                print(f"\n  Query #{analysis['query_id']}: {analysis['execution_time']:.2f}s")
                print(f"  {analysis['query']}")
                print(f"  Issue: {analysis['explanation']}")
        else:
            print("  ✅ No critical issues found")
        
        print("\n⚠️  HIGH PRIORITY ISSUES:")
        high_queries = [a for a in analyses if a['severity'] == 'high']
        if high_queries:
            for analysis in high_queries:
                print(f"\n  Query #{analysis['query_id']}: {analysis['execution_time']:.2f}s")
                print(f"  {analysis['query']}")
                print(f"  Issue: {analysis['explanation']}")
        else:
            print("  ✅ No high priority issues found")
        
        print("\n📊 PERFORMANCE METRICS:")
        summary = self.query_analyzer.generate_query_summary(analyses)
        self._display_query_summary(summary)
        
        print("\n🔧 TOP RECOMMENDATIONS:")
        print("1. Add missing indexes on frequently queried columns")
        print("2. Optimize queries with high row examination ratios")
        print("3. Consider query rewriting for complex subqueries")
        print("4. Implement proper JOIN strategies")
        print("5. Use EXPLAIN ANALYZE to verify optimization results")
        
        print("="*80)
    
    def ask_question(self, question: str) -> None:
        """Ask a question about database performance using OpenAI."""
        print(f"\n🤖 AI Database Consultant")
        print("="*60)
        print(f"Question: {question}")
        print("-" * 60)
        
        gemini_analyzer = self._get_gemini_analyzer()
        
        if gemini_analyzer:
            try:
                answer = gemini_analyzer.ask_question(question)
                print(f"Answer: {answer}")
            except Exception as e:
                print(f"❌ Error getting Gemini response: {e}")
                print("Please check your API key and try again.")
        else:
            print("❌ Gemini Pro is not available. Please check your API key.")
            print("Run: python setup_gemini.py")
        
        print("="*60)
    
    def run_ai_analysis(self) -> None:
        """Run AI-powered analysis on demo queries."""
        print("\n🤖 AI-POWERED QUERY ANALYSIS")
        print("="*80)
        
        gemini_analyzer = self._get_gemini_analyzer()
        
        demo_queries = self.query_analyzer.get_demo_queries(5)
        print(f"Analyzing {len(demo_queries)} queries with Gemini Pro...\n")
        
        if gemini_analyzer:
            try:
                analyses = gemini_analyzer.analyze_multiple_queries(demo_queries)
                self._display_gemini_analyses(analyses)
                
                print("\n" + "="*80)
                print("🤖 GEMINI AI SUMMARY REPORT")
                print("="*80)
                summary = gemini_analyzer.generate_summary_report(analyses)
                print(summary)
                
            except Exception as e:
                print(f"❌ Error during Gemini analysis: {e}")
                print("Please check your API key and try again.")
        else:
            print("❌ Gemini Pro is not available. Please check your API key.")
            print("Run: python setup_gemini.py")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Powered MySQL Observability CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python p3cli.py --monitor              # Collect and display current metrics
  python p3cli.py --analyze              # Run anomaly detection
  python p3cli.py --analyze-queries      # Analyze slow queries with detailed recommendations
  python p3cli.py --query-report         # Generate comprehensive query performance report
  python p3cli.py --ai-analysis          # Run AI-powered query analysis (requires OpenAI)
  python p3cli.py --ask "Why is my query slow?"  # Ask AI about database performance
  python p3cli.py --select-database      # Select which database to work with
  python p3cli.py --config               # Show current configuration
  python p3cli.py --monitor --analyze    # Both monitor and analyze
        """
    )
    
    parser.add_argument('--monitor', action='store_true',
                       help='Collect and display current MySQL metrics')
    parser.add_argument('--analyze', action='store_true',
                       help='Run anomaly detection on current metrics')
    parser.add_argument('--config', action='store_true',
                       help='Show current configuration')
    parser.add_argument('--config-file', default='config.json',
                       help='Path to configuration file (default: config.json)')
    parser.add_argument('--show-history', action='store_true',
                       help='Show metrics history')
    parser.add_argument('--analyze-queries', action='store_true',
                       help='Analyze slow queries with detailed recommendations')
    parser.add_argument('--query-report', action='store_true',
                       help='Generate comprehensive query performance report')
    parser.add_argument('--ask', type=str, metavar='QUESTION',
                       help='Ask a question about database performance (requires OpenAI)')
    parser.add_argument('--ai-analysis', action='store_true',
                       help='Run AI-powered query analysis (requires OpenAI)')
    parser.add_argument('--select-database', action='store_true',
                       help='Select which database to work with')
    
    args = parser.parse_args()
    
    tool = MySQLObservabilityTool(args.config_file)
    
    tool.metrics_history = tool.load_metrics_history()
    
    if args.config:
        tool.show_config()
        return
    
    if args.show_history:
        history = tool.load_metrics_history()
        print(f"\nMetrics History ({len(history)} entries):")
        print("="*60)
        for i, entry in enumerate(history[-10:]):
            print(f"Entry {i+1}:")
            for metric, value in entry.items():
                if metric != 'timestamp':
                    print(f"  {metric}: {value:.2f}")
            print("-"*40)
        return
    
    if args.analyze_queries:
        tool.analyze_queries()
        return
    
    if args.query_report:
        tool.generate_query_report()
        return
    
    if args.ask:
        tool.ask_question(args.ask)
        return
    
    if args.ai_analysis:
        tool.run_ai_analysis()
        return
    
    if args.select_database:
        import subprocess
        subprocess.run([sys.executable, 'select_database.py'])
        return
    
    if not (args.monitor or args.analyze):
        parser.print_help()
        return
    
    print("Collecting MySQL metrics...")
    current_metrics = tool.collect_metrics()
    
    if not current_metrics:
        print("MySQL connection failed. Switching to demo mode...")
        current_metrics = tool.collect_metrics(demo_mode=True)
        if not current_metrics:
            print("Failed to collect metrics even in demo mode.")
            sys.exit(1)
    
    tool.save_metrics(current_metrics)
    
    if args.monitor:
        print("Collecting 100 MySQL metrics samples...")
        for i in range(100):
                 current_metrics = tool.collect_metrics()
                 if not current_metrics:
                   print("MySQL connection failed. Switching to demo mode...")
                   current_metrics = tool.collect_metrics(demo_mode=True)
                 if not current_metrics:
                    print("Failed to collect metrics even in demo mode.")
                    sys.exit(1)
                 tool.save_metrics(current_metrics)

        # Show only the last collected datapoint
        tool.display_metrics(current_metrics)
    
    if args.analyze:
        print("\nRunning anomaly detection...")
        print(f"Analyzing current metrics:")
        for metric, value in current_metrics.items():
            if metric != 'timestamp':
                print(f"  {metric}: {value:.2f}")
        
        if len(tool.metrics_history) >= tool.config["ml"]["min_samples_for_training"]:
            tool.train_anomaly_model(tool.metrics_history)
            
            is_anomaly, score = tool.detect_anomalies(current_metrics)
            
            print("\n" + "="*50)
            print("Anomaly Detection Results")
            print("="*50)
            
            if is_anomaly:
                print("⚠️  ANOMALY DETECTED!")
                print(f"Anomaly Score: {score:.4f}")
                print("The current metrics show unusual patterns that may indicate:")
                print("- Performance degradation")
                print("- Resource contention")
                print("- Potential issues requiring attention")
            else:
                print("✅ Metrics appear normal")
                print(f"Anomaly Score: {score:.4f}")
            
            print("="*50)
        else:
            print(f"Need at least {tool.config['ml']['min_samples_for_training']} data points for anomaly detection.")
            print(f"Currently have: {len(tool.metrics_history)} data points.")
            print("Run --monitor a few more times to collect training data.")


if __name__ == "__main__":
    main()
