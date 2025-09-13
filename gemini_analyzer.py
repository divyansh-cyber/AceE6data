#!/usr/bin/env python3
"""
Google Gemini Pro Query Analysis Module

This module provides AI-powered query analysis using Google's Gemini Pro API:
- Natural language understanding of SQL queries
- Dynamic performance analysis and recommendations
- Conversational interface for database optimization
- Cost-effective alternative to OpenAI
"""

import json
import os
from typing import Dict, List, Optional
import google.generativeai as genai

class GeminiAnalyzer:
    """Gemini Pro-powered query analysis and recommendation engine."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini analyzer."""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System prompts for different analysis types
        self.system_prompts = {
            'query_analysis': """You are an expert MySQL database performance consultant. Analyze the given query and provide detailed insights about:

1. Why the query is slow (specific technical reasons)
2. What indexes should be added (with CREATE INDEX statements)
3. Query optimization opportunities
4. Estimated performance improvement
5. Best practices for this type of query

Be specific, technical, and provide actionable recommendations. Use MySQL-specific terminology and best practices.""",

            'conversational': """You are a helpful MySQL database performance expert. Answer questions about database optimization, query performance, and MySQL best practices. 

Provide clear, technical explanations that both beginners and experts can understand. Include specific examples and code snippets when relevant.""",

            'recommendations': """You are a MySQL performance expert. Based on the query analysis, provide specific, actionable recommendations including:

1. Exact CREATE INDEX statements
2. Query rewriting suggestions
3. Configuration optimizations
4. Performance monitoring advice

Be precise and provide ready-to-use SQL statements."""
        }
    
    def analyze_query(self, query: str, metrics: Dict) -> Dict:
        """Analyze a single query using Gemini Pro."""
        try:
            prompt = f"""
Query: {query}
Execution Time: {metrics.get('execution_time', 0):.2f}s
Rows Examined: {metrics.get('rows_examined', 0):,}
Rows Sent: {metrics.get('rows_sent', 0):,}
Efficiency: {metrics.get('efficiency_ratio', 0):.2%}

Please analyze this query and provide:
1. Why it's slow (specific technical reasons)
2. What indexes to add (with CREATE INDEX statements)
3. Query optimization suggestions
4. Estimated performance improvement
5. Severity level (Critical/High/Medium/Low)
"""
            
            response = self.model.generate_content(
                f"{self.system_prompts['query_analysis']}\n\n{prompt}"
            )
            
            analysis_text = response.text
            
            # Parse the response to extract structured information
            return self._parse_analysis_response(analysis_text, query, metrics)
            
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
        """Answer a conversational question about database performance."""
        try:
            # Load recent analysis data as context
            analysis_context = self._get_recent_analysis_context()
            
            context_str = ""
            if context:
                context_str = f"\n\nSpecific Context:\nQuery: {context.get('query', 'N/A')}\nExecution Time: {context.get('execution_time', 0):.2f}s\nRows Examined: {context.get('rows_examined', 0):,}"
            
            full_context = f"{self.system_prompts['conversational']}\n\n{analysis_context}\n\n{question}{context_str}"
            
            response = self.model.generate_content(full_context)
            
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _get_recent_analysis_context(self) -> str:
        """Get recent analysis data to provide as context for questions."""
        try:
            # Try to load recent analysis from a cache file
            import json
            import os
            
            if os.path.exists('recent_analysis.json'):
                with open('recent_analysis.json', 'r') as f:
                    recent_data = json.load(f)
                
                context = f"""CURRENT DATABASE ANALYSIS CONTEXT:

Recent Query Analysis Results:
- Total Queries Analyzed: {recent_data.get('total_queries', 0)}
- Slow Queries: {recent_data.get('slow_queries', 0)}
- Critical Issues: {recent_data.get('critical_issues', 0)}
- Average Execution Time: {recent_data.get('avg_execution_time', 0):.2f}s

Recent Slow Queries:
"""
                
                for i, query in enumerate(recent_data.get('queries', [])[:5], 1):
                    context += f"Query #{i}: {query.get('query', 'N/A')[:60]}...\n"
                    context += f"  - Execution Time: {query.get('execution_time', 0):.2f}s\n"
                    context += f"  - Rows Examined: {query.get('rows_examined', 0):,}\n"
                    context += f"  - Severity: {query.get('severity', 'unknown')}\n"
                    context += f"  - Main Issue: {query.get('main_issue', 'N/A')}\n\n"
                
                return context
            else:
                return "No recent analysis data available. Run --analyze-queries first to get context."
                
        except Exception as e:
            return f"Error loading analysis context: {str(e)}"
    
    def generate_recommendations(self, query: str, issues: List[str]) -> List[str]:
        """Generate specific recommendations for query optimization."""
        try:
            prompt = f"""
Query: {query}
Identified Issues: {', '.join(issues)}

Provide specific, actionable recommendations including:
1. Exact CREATE INDEX statements
2. Query rewriting suggestions
3. Configuration optimizations
4. Performance monitoring advice

Format as a numbered list with ready-to-use SQL statements.
"""
            
            response = self.model.generate_content(
                f"{self.system_prompts['recommendations']}\n\n{prompt}"
            )
            
            # Parse recommendations into a list
            recommendations_text = response.text
            return self._parse_recommendations(recommendations_text)
            
        except Exception as e:
            return [f"Error generating recommendations: {str(e)}"]
    
    def _parse_analysis_response(self, analysis_text: str, query: str, metrics: Dict) -> Dict:
        """Parse Gemini response into structured format."""
        # Extract severity level
        severity = 'medium'
        if 'critical' in analysis_text.lower():
            severity = 'critical'
        elif 'high' in analysis_text.lower():
            severity = 'high'
        elif 'low' in analysis_text.lower():
            severity = 'low'
        
        # Extract CREATE INDEX statements
        indexes = []
        lines = analysis_text.split('\n')
        for line in lines:
            if 'CREATE INDEX' in line.upper() or 'CREATE UNIQUE INDEX' in line.upper():
                indexes.append(line.strip())
        
        # Extract recommendations
        recommendations = self._parse_recommendations(analysis_text)
        
        # Extract performance improvement estimate
        improvement = "Unknown"
        for line in lines:
            if any(word in line.lower() for word in ['improvement', 'faster', 'reduce', 'optimize']):
                improvement = line.strip()
                break
        
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
        """Parse recommendations from text into a list."""
        recommendations = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or 
                        line.startswith(('•', '-', '*')) or
                        line.startswith(('CREATE', 'ALTER', 'OPTIMIZE'))):
                # Clean up the line
                line = line.lstrip('123456789.•-* ').strip()
                if line:
                    recommendations.append(line)
        
        return recommendations[:10]  # Limit to 10 recommendations
    
    def analyze_multiple_queries(self, queries: List[Dict]) -> List[Dict]:
        """Analyze multiple queries using Gemini Pro."""
        results = []
        
        for i, query_data in enumerate(queries):
            print(f"Analyzing query {i+1}/{len(queries)}...")
            
            # Prepare metrics
            metrics = {
                'execution_time': query_data.get('execution_time', 0),
                'rows_examined': query_data.get('rows_examined', 0),
                'rows_sent': query_data.get('rows_sent', 0),
                'efficiency_ratio': query_data.get('rows_sent', 0) / max(query_data.get('rows_examined', 1), 1)
            }
            
            analysis = self.analyze_query(query_data['query'], metrics)
            results.append(analysis)
        
        # Save analysis data for context in future questions
        self._save_analysis_context(results)
        
        return results
    
    def _save_analysis_context(self, analyses: List[Dict]) -> None:
        """Save analysis data for use as context in future questions."""
        try:
            import json
            
            # Prepare summary data
            total_queries = len(analyses)
            slow_queries = sum(1 for a in analyses if a.get('execution_time', 0) > 2.0)
            critical_issues = sum(1 for a in analyses if a.get('severity') == 'critical')
            avg_execution_time = sum(a.get('execution_time', 0) for a in analyses) / len(analyses)
            
            # Extract main issues from AI analysis
            queries_data = []
            for analysis in analyses:
                main_issue = "Unknown"
                if 'ai_analysis' in analysis:
                    # Extract the main issue from the AI analysis
                    analysis_text = analysis['ai_analysis']
                    if 'Why it' in analysis_text:
                        # Try to extract the main reason
                        lines = analysis_text.split('\n')
                        for line in lines:
                            if 'Why it' in line or 'Why the query is slow' in line:
                                main_issue = line.strip()
                                break
                
                queries_data.append({
                    'query': analysis.get('query', ''),
                    'execution_time': analysis.get('execution_time', 0),
                    'rows_examined': analysis.get('rows_examined', 0),
                    'severity': analysis.get('severity', 'unknown'),
                    'main_issue': main_issue
                })
            
            # Save to file
            context_data = {
                'total_queries': total_queries,
                'slow_queries': slow_queries,
                'critical_issues': critical_issues,
                'avg_execution_time': avg_execution_time,
                'queries': queries_data,
                'timestamp': __import__('time').time()
            }
            
            with open('recent_analysis.json', 'w') as f:
                json.dump(context_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save analysis context: {e}")
    
    def generate_summary_report(self, analyses: List[Dict]) -> str:
        """Generate a comprehensive summary report."""
        try:
            # Prepare summary data
            total_queries = len(analyses)
            slow_queries = sum(1 for a in analyses if a.get('execution_time', 0) > 2.0)
            critical_issues = sum(1 for a in analyses if a.get('severity') == 'critical')
            high_issues = sum(1 for a in analyses if a.get('severity') == 'high')
            
            # Get all unique indexes recommended
            all_indexes = []
            for analysis in analyses:
                all_indexes.extend(analysis.get('indexes', []))
            unique_indexes = list(set(all_indexes))
            
            prompt = f"""
Generate a comprehensive MySQL performance report based on this analysis:

Total Queries: {total_queries}
Slow Queries (>2s): {slow_queries}
Critical Issues: {critical_issues}
High Priority Issues: {high_issues}

Key Issues Found:
{chr(10).join([f"- {a.get('query', 'N/A')[:50]}... ({a.get('severity', 'unknown')})" for a in analyses[:5]])}

Recommended Indexes:
{chr(10).join(unique_indexes[:10])}

Provide:
1. Executive summary
2. Top 3 critical issues
3. Priority recommendations
4. Expected performance improvements
5. Next steps for optimization
"""
            
            response = self.model.generate_content(
                f"You are a senior database consultant. Generate a professional performance report.\n\n{prompt}"
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating summary report: {str(e)}"
