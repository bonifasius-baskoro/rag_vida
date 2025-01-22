import sqlite3
from db.db_instance import get_db
from exception.DatabaseException import DatabaseError
def execute_query(query):
    """Execute custom SQL query"""
    try:

        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            results = [dict(row) for row in rows]
            
            return results
            
        except sqlite3.Error as e:
            string_error = f'error : SQL error: {str(e)}'
            return string_error
            
        finally:
            conn.close()
            
    except Exception as e:
        raise DatabaseError(f"Failed to query database: {str(e)}")