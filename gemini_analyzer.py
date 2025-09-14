#!/usr/bin/env python3
"""
Google Gemini Pro Query Analysis Module

Provides AI-powered query analysis using Google's Gemini Pro API:
- SQL query understanding
- Performance analysis and recommendations
- Conversational database optimization interface
- Cost-effective alternative to OpenAI
"""

import json
import os
from typing import Dict, List, Optional
import google.generativeai as genai

class GeminiAnalyzer:
    """Gemini Pro-powered query analysis and recommendation engine."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY or pass api_key parameter.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.system_prompts = {
            'query_analysis': """You are an expert MySQL database performance consultant. Analyze the given query and provide detailed insights about:
1. Why the query is slow (specific technical reasons)
2. What indexes should be added (with CREATE INDEX statements)
3. Query optimization opportunities
4. Estimated performance improvement
5. Best practices for this type of query""",

            'conversational': """You are a helpful MySQL database performance expert. Answer questions about database optimization, query performance, and MySQL best practices with clear, technical explanations.""",

            'recommendations': """You are a MySQL performance expert. Based on the query analysis, provide:
1. Exact CREATE INDEX statements
2. Query rewriting suggestions
3. Configuration optimizations
4. Performance monitoring advice"""
        }
    
    def analyze_query(self, query: str, metrics: Dict) -> Dict:
        try:
            prompt = f"""
Query: {query}
Execution Time: {metrics.get('execution_time', 0):.2f}s
Rows Examined: {metrics.get('rows_examined', 0):,}
Rows Sent: {metrics.get('rows_sent', 0):,}
Efficiency: {metrics.get('efficiency_ratio', 0):.2%}

Please analyze this query and provide:
1. Reasons for slowness
2. Recommended indexes
3. Query optimization suggestions
4. Estimated performance improvement
5. Severity (Critical/High/Medium/Low)
"""
            response = self.model.generate_content(
                f"{self.system_prompts['query_analysis']}\n\n{prompt}"
            )
            return self._parse_analysis_response(response.text, query, metrics)
        except Exception as e:
            return {
                'query': query,
                'execution_time': metrics.get('execution_time', 0),
                'rows_examined': metrics.get('rows_examined', 0),
                'rows_sent': metrics.get('rows_sent', 0),
                'ai_analysis': f"Error analyzing query: {str(e)}",
                'severity': 'unknown',
                'recommendations': ["Unable to analyze due to API error"],
                'indexes': [],
                'estimated_improvement': "Unknown"
            }
    
    def ask_question(self, question: str, context: Optional[Dict] = None) -> str:
        try:
            analysis_context = self._get_recent_analysis_context()
            context_str = ""
            if context:
                context_str = f"\n\nQuery: {context.get('query', 'N/A')}\nExecution Time: {context.get('execution_time', 0):.2f}s\nRows Examined: {context.get('rows_examined', 0):,}"
            full_context = f"{self.system_prompts['conversational']}\n\n{analysis_context}\n\n{question}{context_str}"
            return self.model.generate_content(full_context).text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _get_recent_analysis_context(self) -> str:
        try:
            if os.path.exists('recent_analysis.json'):
                with open('recent_analysis.json', 'r') as f:
                    recent_data = json.load(f)
                context = f"""CURRENT DATABASE CONTEXT:
Total Queries Analyzed: {recent_data.get('total_queries', 0)}
Slow Queries: {recent_data.get('slow_queries', 0)}
Critical Issues: {recent_data.get('critical_issues', 0)}
Average Execution Time: {recent_data.get('avg_execution_time', 0):.2f}s

Recent Slow Queries:
"""
                for i, query in enumerate(recent_data.get('queries', [])[:5], 1):
                    context += f"Query #{i}: {query.get('query', 'N/A')[:60]}...\n"
                    context += f"  Execution Time: {query.get('execution_time', 0):.2f}s\n"
                    context += f"  Rows Examined: {query.get('rows_examined', 0):,}\n"
                    context += f"  Severity: {query.get('severity', 'unknown')}\n"
                    context += f"  Main Issue: {query.get('main_issue', 'N/A')}\n\n"
                return context
            return "No recent analysis data available."
        except Exception as e:
            return f"Error loading context: {str(e)}"
    
    def generate_recommendations(self, query: str, issues: List[str]) -> List[str]:
        try:
            prompt = f"""
Query: {query}
Issues: {', '.join(issues)}

Provide:
1. CREATE INDEX statements
2. Query rewriting suggestions
3. Config optimizations
4. Monitoring advice
"""
            response = self.model.generate_content(
                f"{self.system_prompts['recommendations']}\n\n{prompt}"
            )
            return self._parse_recommendations(response.text)
        except Exception as e:
            return [f"Error generating recommendations: {str(e)}"]
    
    def _parse_analysis_response(self, analysis_text: str, query: str, metrics: Dict) -> Dict:
        severity = 'medium'
        if 'critical' in analysis_text.lower():
            severity = 'critical'
        elif 'high' in analysis_text.lower():
            severity = 'high'
        elif 'low' in analysis_text.lower():
            severity = 'low'
        
        indexes = [line.strip() for line in analysis_text.split('\n') if 'CREATE INDEX' in line.upper()]
        recommendations = self._parse_recommendations(analysis_text)
        improvement = next((line.strip() for line in analysis_text.split('\n') if any(word in line.lower() for word in ['improvement', 'faster', 'reduce', 'optimize'])), "Unknown")
        
        return {
            'query': query,
            'execution_time': metrics.get('execution_time', 0),
            'rows_examined': metrics.get('rows_examined', 0),
            'rows_sent': metrics.get('rows_sent', 0),
            'efficiency_ratio': metrics.get('rows_sent', 0) / max(metrics.get('rows_examined', 1), 1),
            'ai_analysis': analysis_text,
            'severity': severity,
            'recommendations': recommendations,
            'indexes': indexes,
            'estimated_improvement': improvement
        }
    
    def _parse_recommendations(self, text: str) -> List[str]:
        recommendations = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line.startswith(tuple(f"{i}." for i in range(1, 10))) or 
                         line.startswith(('•', '-', '*')) or
                         line.upper().startswith(('CREATE', 'ALTER', 'OPTIMIZE'))):
                recommendations.append(line.lstrip('123456789.•-* ').strip())
        return recommendations[:10]
    
    def analyze_multiple_queries(self, queries: List[Dict]) -> List[Dict]:
        results = []
        for query_data in queries:
            metrics = {
                'execution_time': query_data.get('execution_time', 0),
                'rows_examined': query_data.get('rows_examined', 0),
                'rows_sent': query_data.get('rows_sent', 0),
                'efficiency_ratio': query_data.get('rows_sent', 0) / max(query_data.get('rows_examined', 1), 1)
            }
            results.append(self.analyze_query(query_data['query'], metrics))
        self._save_analysis_context(results)
        return results
    
    def _save_analysis_context(self, analyses: List[Dict]) -> None:
        try:
            total_queries = len(analyses)
            slow_queries = sum(1 for a in analyses if a.get('execution_time', 0) > 2.0)
            critical_issues = sum(1 for a in analyses if a.get('severity') == 'critical')
            avg_execution_time = sum(a.get('execution_time', 0) for a in analyses) / len(analyses)
            queries_data = []
            for analysis in analyses:
                main_issue = "Unknown"
                if 'ai_analysis' in analysis:
                    for line in analysis['ai_analysis'].split('\n'):
                        if 'Why' in line:
                            main_issue = line.strip()
                            break
                queries_data.append({
                    'query': analysis.get('query', ''),
                    'execution_time': analysis.get('execution_time', 0),
                    'rows_examined': analysis.get('rows_examined', 0),
                    'severity': analysis.get('severity', 'unknown'),
                    'main_issue': main_issue
                })
            with open('recent_analysis.json', 'w') as f:
                json.dump({
                    'total_queries': total_queries,
                    'slow_queries': slow_queries,
                    'critical_issues': critical_issues,
                    'avg_execution_time': avg_execution_time,
                    'queries': queries_data,
                    'timestamp': __import__('time').time()
                }, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save analysis context: {e}")
    
    def generate_summary_report(self, analyses: List[Dict]) -> str:
        try:
            total_queries = len(analyses)
            slow_queries = sum(1 for a in analyses if a.get('execution_time', 0) > 2.0)
            critical_issues = sum(1 for a in analyses if a.get('severity') == 'critical')
            high_issues = sum(1 for a in analyses if a.get('severity') == 'high')
            all_indexes = list({idx for a in analyses for idx in a.get('indexes', [])})
            prompt = f"""
Generate a professional MySQL performance report:

Total Queries: {total_queries}
Slow Queries (>2s): {slow_queries}
Critical Issues: {critical_issues}
High Priority Issues: {high_issues}

Top Issues:
{chr(10).join([f"- {a.get('query', '')[:50]}... ({a.get('severity', 'unknown')})" for a in analyses[:5]])}

Recommended Indexes:
{chr(10).join(all_indexes[:10])}
"""
            return self.model.generate_content(
                f"You are a senior database consultant. Generate a professional performance report.\n\n{prompt}"
            ).text
        except Exception as e:
            return f"Error generating summary report: {str(e)}"
