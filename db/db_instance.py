import sqlite3
import pandas as pd
import os
from typing import Optional, List, Dict, Any


DATABASE_NAME = 'credit_data.db'

def init_db_from_csv(csv_file_path):
    """Initialize SQLite database from CSV file"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Create SQLite database
        conn = sqlite3.connect(DATABASE_NAME)
        
        # Get table name from CSV filename without extension
        table_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        print(table_name)
        # Write to SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"Database initialized with table: {table_name}")
        conn.close()
        return table_name
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return None
    
def init_credit_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'credit_data.csv')
    table_name = init_db_from_csv(csv_path)
    return table_name

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn