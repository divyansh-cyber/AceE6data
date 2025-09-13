import gradio as gr
import pandas as pd
import sqlite3
from typing import List, Tuple, Optional
import json
import sys
import os

# Import your existing SQL analysis functions
# from your_cli_module import run_sql_query, get_database_info, etc.

# Mock functions (replace with your actual functions)
def get_available_databases() -> List[str]:
    # Replace with actual implementation to get available databases
    return ["sample_db1.db", "sample_db2.db"]

def run_sql_query(db_path: str, query: str) -> Tuple[pd.DataFrame, Optional[str]]:
    """Run a SQL query and return results as DataFrame or error message"""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return pd.DataFrame(), str(e)

def get_table_schema(db_path: str) -> dict:
    """Get schema information for all tables in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        schema[table] = [
            {"name": col[1], "type": col[2], "notnull": col[3], "pk": col[5]}
            for col in columns
        ]
    
    conn.close()
    return schema

def process_ai_query(db_path: str, question: str) -> Tuple[str, Optional[pd.DataFrame]]:
    """Process natural language query using your AI assistant"""
    # This would connect to your existing conversational AI assistant
    # For now, return a placeholder
    sql_query = f"SELECT * FROM some_table LIMIT 5;  -- Generated from: '{question}'"
    df, error = run_sql_query(db_path, sql_query)
    if error:
        return f"Error: {error}", None
    else:
        return sql_query, df

# Gradio Interface Functions
def select_database(db_name):
    """When user selects a database, return its schema"""
    if not db_name:
        return "Please select a database", None, None
    
    try:
        schema = get_table_schema(db_name)
        schema_text = json.dumps(schema, indent=2)
        return f"Connected to {db_name}", schema_text, db_name
    except Exception as e:
        return f"Error connecting to database: {str(e)}", None, None

def execute_query(db_path, query):
    """Execute SQL query and return results"""
    if not db_path or not query:
        return "Please select a database and enter a query", None
    
    df, error = run_sql_query(db_path, query)
    if error:
        return f"Error: {error}", None
    
    # Check if dataframe is empty
    if df.empty:
        return "Query executed successfully but returned no results.", None
    
    return "Query executed successfully", df

def ask_ai_assistant(db_path, question):
    """Ask AI assistant a natural language question"""
    if not db_path or not question:
        return "Please select a database and ask a question", None, None
    
    generated_sql, results = process_ai_query(db_path, question)
    
    if results is None:
        return generated_sql, None, None
    
    return f"Generated SQL Query:\n{generated_sql}", results, generated_sql

# Create Gradio Interface
with gr.Blocks(title="AceE6data SQL Analysis Dashboard") as demo:
    gr.Markdown("# AceE6data SQL Analysis Dashboard")
    
    # Track the selected database path
    db_path_state = gr.State(value=None)
    
    with gr.Tab("Database Explorer"):
        with gr.Row():
            with gr.Column(scale=1):
                db_dropdown = gr.Dropdown(
                    choices=get_available_databases(),
                    label="Select Database",
                    interactive=True
                )
                db_status = gr.Textbox(label="Status", interactive=False)
            
            with gr.Column(scale=2):
                schema_json = gr.JSON(label="Database Schema")
        
        connect_btn = gr.Button("Connect")
        connect_btn.click(
            fn=select_database,
            inputs=[db_dropdown],
            outputs=[db_status, schema_json, db_path_state]
        )
    
    with gr.Tab("SQL Query"):
        with gr.Row():
            sql_query = gr.Textbox(
                label="Enter SQL Query",
                placeholder="SELECT * FROM your_table LIMIT 10;",
                lines=5
            )
        
        query_btn = gr.Button("Execute Query")
        query_status = gr.Textbox(label="Query Status", interactive=False)
        query_results = gr.DataFrame(label="Results")
        
        query_btn.click(
            fn=execute_query,
            inputs=[db_path_state, sql_query],
            outputs=[query_status, query_results]
        )
    
    with gr.Tab("AI Assistant"):
        with gr.Row():
            question = gr.Textbox(
                label="Ask a question about your data",
                placeholder="Show me sales trends for the last month",
                lines=2
            )
        
        ask_btn = gr.Button("Ask AI")
        ai_response = gr.Textbox(label="AI Response", interactive=False)
        ai_results = gr.DataFrame(label="Results")
        generated_query = gr.Textbox(label="Generated Query", visible=False)
        
        ask_btn.click(
            fn=ask_ai_assistant,
            inputs=[db_path_state, question],
            outputs=[ai_response, ai_results, generated_query]
        )
        
        with gr.Row(visible=False) as sql_edit_row:
            edit_sql = gr.Button("Edit Generated SQL")
            
        def show_edit_sql():
            return {
                sql_edit_row: gr.update(visible=True),
                sql_query: gr.update(value=generated_query.value)
            }
            
        edit_sql.click(
            fn=show_edit_sql,
            inputs=None,
            outputs=[sql_edit_row, sql_query]
        )

# Launch the app
if __name__ == "__main__":
    demo.launch()