#!/usr/bin/env python3
"""
Advanced Query Analysis Module for MySQL Observability Tool

This module provides detailed analysis of individual queries, including:
- Slow query detection with specific reasons
- Missing index recommendations
- Query optimization suggestions
- Performance bottleneck identification
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import re

class QueryAnalyzer:
    """Advanced query analysis and recommendation engine."""
    
    def __init__(self):
        self.slow_query_threshold = 2.0  # seconds
        self.query_patterns = {
            'missing_index': [
                r'WHERE\s+\w+\s*=\s*\?',  # Simple equality without index
                r'WHERE\s+\w+\s+IN\s*\(',  # IN clause without index
                r'ORDER\s+BY\s+\w+',  # ORDER BY without index
                r'GROUP\s+BY\s+\w+',  # GROUP BY without index
            ],
            'full_table_scan': [
                r'WHERE\s+\w+\s+LIKE\s+[\'"]%',  # LIKE with leading wildcard
                r'WHERE\s+\w+\s+!=',  # Not equal without index
                r'WHERE\s+\w+\s+NOT\s+IN',  # NOT IN without index
            ],
            'inefficient_joins': [
                r'CROSS\s+JOIN',  # Cross joins
                r'LEFT\s+JOIN.*WHERE.*IS\s+NULL',  # Anti-joins
                r'JOIN.*ON\s+\w+\.\w+\s*=\s*\w+\.\w+.*AND',  # Complex join conditions
            ],
            'subquery_issues': [
                r'WHERE\s+\w+\s+IN\s*\(SELECT',  # IN subquery
                r'WHERE\s+EXISTS\s*\(SELECT',  # EXISTS subquery
                r'SELECT.*FROM\s*\(SELECT',  # Nested subqueries
            ]
        }
        
        # Sample problematic queries for demo
        self.demo_queries = [
            {
                'id': 1001,
                'query': "SELECT * FROM users WHERE email = 'user@example.com'",
                'execution_time': 0.5,
                'rows_examined': 1000000,
                'rows_sent': 1,
                'issues': ['missing_index'],
                'explanation': "Query is slow because there's no index on the 'email' column, causing a full table scan of 1M rows."
            },
            {
                'id': 1002,
                'query': "SELECT u.*, p.* FROM users u LEFT JOIN posts p ON u.id = p.user_id WHERE u.created_at > '2024-01-01'",
                'execution_time': 3.2,
                'rows_examined': 5000000,
                'rows_sent': 50000,
                'issues': ['missing_index', 'inefficient_joins'],
                'explanation': "Query is slow because: 1) No index on 'created_at' column, 2) LEFT JOIN without proper indexing on foreign key 'p.user_id'"
            },
            {
                'id': 1003,
                'query': "SELECT * FROM orders WHERE status IN ('pending', 'processing', 'shipped') ORDER BY created_at DESC",
                'execution_time': 1.8,
                'rows_examined': 2000000,
                'rows_sent': 10000,
                'issues': ['missing_index'],
                'explanation': "Query is slow because there's no composite index on (status, created_at) columns for efficient filtering and sorting."
            },
            {
                'id': 1004,
                'query': "SELECT * FROM products WHERE name LIKE '%laptop%' AND category_id = 5",
                'execution_time': 4.5,
                'rows_examined': 3000000,
                'rows_sent': 500,
                'issues': ['full_table_scan', 'missing_index'],
                'explanation': "Query is slow because: 1) LIKE with leading wildcard '%laptop%' prevents index usage, 2) No composite index on (category_id, name)"
            },
            {
                'id': 1005,
                'query': "SELECT COUNT(*) FROM orders o WHERE EXISTS (SELECT 1 FROM order_items oi WHERE oi.order_id = o.id AND oi.quantity > 10)",
                'execution_time': 2.1,
                'rows_examined': 1000000,
                'rows_sent': 1,
                'issues': ['subquery_issues'],
                'explanation': "Query is slow because EXISTS subquery is not optimized. Consider using JOIN instead of EXISTS for better performance."
            },
            {
                'id': 1006,
                'query': "SELECT * FROM users WHERE age BETWEEN 18 AND 65 AND city = 'New York' ORDER BY last_login DESC LIMIT 100",
                'execution_time': 0.8,
                'rows_examined': 500000,
                'rows_sent': 100,
                'issues': ['missing_index'],
                'explanation': "Query is slow because there's no composite index on (city, age, last_login) for efficient filtering, sorting, and limiting."
            },
            {
                'id': 1007,
                'query': "SELECT u.name, COUNT(p.id) as post_count FROM users u LEFT JOIN posts p ON u.id = p.user_id GROUP BY u.id HAVING post_count > 10",
                'execution_time': 2.8,
                'rows_examined': 4000000,
                'rows_sent': 5000,
                'issues': ['missing_index', 'inefficient_joins'],
                'explanation': "Query is slow because: 1) No index on foreign key 'p.user_id', 2) GROUP BY without proper indexing, 3) Consider adding covering index on (user_id, id)"
            },
            {
                'id': 1008,
                'query': "SELECT * FROM logs WHERE log_level = 'ERROR' AND created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY) ORDER BY created_at DESC",
                'execution_time': 1.2,
                'rows_examined': 800000,
                'rows_sent': 2000,
                'issues': ['missing_index'],
                'explanation': "Query is slow because there's no composite index on (log_level, created_at) for efficient filtering and sorting."
            },
            {
                'id': 1009,
                'query': "UPDATE products SET price = price * 1.1 WHERE category_id = 3 AND in_stock = 1",
                'execution_time': 3.5,
                'rows_examined': 1500000,
                'rows_sent': 0,
                'issues': ['missing_index'],
                'explanation': "Query is slow because there's no composite index on (category_id, in_stock) for efficient filtering during UPDATE operation."
            },
            {
                'id': 1010,
                'query': "SELECT DISTINCT user_id FROM orders WHERE total_amount > 1000 AND created_at > '2024-01-01'",
                'execution_time': 2.3,
                'rows_examined': 2000000,
                'rows_sent': 15000,
                'issues': ['missing_index'],
                'explanation': "Query is slow because there's no composite index on (total_amount, created_at, user_id) for efficient filtering and DISTINCT operation."
            }
        ]
    
    def analyze_query_performance(self, query_data: Dict) -> Dict:
        """Analyze a single query and provide detailed recommendations."""
        analysis = {
            'query_id': query_data['id'],
            'query': query_data['query'],
            'execution_time': query_data['execution_time'],
            'rows_examined': query_data['rows_examined'],
            'rows_sent': query_data['rows_sent'],
            'is_slow': query_data['execution_time'] > self.slow_query_threshold,
            'efficiency_ratio': query_data['rows_sent'] / query_data['rows_examined'] if query_data['rows_examined'] > 0 else 0,
            'issues': [],
            'recommendations': [],
            'explanation': query_data.get('explanation', ''),
            'severity': 'low'
        }
        
        # Determine severity
        if query_data['execution_time'] > 5.0 or query_data['rows_examined'] > 5000000:
            analysis['severity'] = 'critical'
        elif query_data['execution_time'] > 2.0 or query_data['rows_examined'] > 1000000:
            analysis['severity'] = 'high'
        elif query_data['execution_time'] > 1.0 or query_data['rows_examined'] > 100000:
            analysis['severity'] = 'medium'
        
        # Analyze specific issues
        for issue_type, patterns in self.query_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_data['query'], re.IGNORECASE):
                    analysis['issues'].append(issue_type)
                    break
        
        # Generate recommendations based on issues
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate specific recommendations based on detected issues."""
        recommendations = []
        
        if 'missing_index' in analysis['issues']:
            recommendations.append("🔍 Add appropriate indexes to improve query performance")
            recommendations.append("📊 Consider composite indexes for multi-column WHERE clauses")
        
        if 'full_table_scan' in analysis['issues']:
            recommendations.append("⚠️ Avoid LIKE patterns with leading wildcards")
            recommendations.append("🔧 Consider full-text search indexes for text searching")
        
        if 'inefficient_joins' in analysis['issues']:
            recommendations.append("🔗 Optimize JOIN conditions and add foreign key indexes")
            recommendations.append("📈 Consider query rewriting for better performance")
        
        if 'subquery_issues' in analysis['issues']:
            recommendations.append("🔄 Consider rewriting subqueries as JOINs")
            recommendations.append("⚡ Use EXISTS only when necessary, prefer JOINs for better performance")
        
        if analysis['efficiency_ratio'] < 0.01:
            recommendations.append("📉 Very low efficiency ratio - consider adding WHERE clauses to reduce examined rows")
        
        if analysis['execution_time'] > 2.0:
            recommendations.append("⏱️ Query execution time exceeds 2 seconds - immediate optimization needed")
        
        return recommendations
    
    def get_demo_queries(self, count: int = 10) -> List[Dict]:
        """Get demo queries for testing."""
        return random.sample(self.demo_queries, min(count, len(self.demo_queries)))
    
    def generate_query_summary(self, analyses: List[Dict]) -> Dict:
        """Generate a summary of all query analyses."""
        total_queries = len(analyses)
        slow_queries = sum(1 for a in analyses if a['is_slow'])
        critical_queries = sum(1 for a in analyses if a['severity'] == 'critical')
        high_priority_queries = sum(1 for a in analyses if a['severity'] in ['critical', 'high'])
        
        issue_counts = {}
        for analysis in analyses:
            for issue in analysis['issues']:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        return {
            'total_queries': total_queries,
            'slow_queries': slow_queries,
            'critical_queries': critical_queries,
            'high_priority_queries': high_priority_queries,
            'slow_query_percentage': (slow_queries / total_queries * 100) if total_queries > 0 else 0,
            'issue_counts': issue_counts,
            'avg_execution_time': sum(a['execution_time'] for a in analyses) / total_queries if total_queries > 0 else 0,
            'total_rows_examined': sum(a['rows_examined'] for a in analyses),
            'total_rows_sent': sum(a['rows_sent'] for a in analyses)
        }
