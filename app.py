from flask import Flask, request, jsonify
import service.chat
from service.decider import rag_decider_agent
from db.db_instance import init_credit_db,get_db
import sqlite3

app = Flask(__name__)
PORT = 5050  # You can change this port number as needed

@app.route('/api', methods=['GET', 'POST'])
def handle_requests():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        chat_input = data['chat']
        chat_result = rag_decider_agent(chat_input)
        # Handle POST request data here
        return jsonify({"message": "POST request received", "data": chat_result}), 200
    
    elif request.method == 'GET':
        # Handle GET request here
        return jsonify({"message": "GET request received"}), 200

@app.route('/api/v1/chat', methods=['GET', 'POST'])
def handle_requests_chat():
    if request.method == 'POST':
        data = request.get_json()
        
        # Handle POST request data here
        return jsonify({"message": "POST request received", "data": data}), 200
    
    elif request.method == 'GET':
        # Handle GET request here
        return jsonify({"message": "GET request received"}), 200


@app.route('/query', methods=['POST'])
def execute_query():
    """Execute custom SQL query"""
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            results = [dict(row) for row in rows]
            
            return jsonify({
                'status': 'success',
                'results': results,
                'row_count': len(results)
            })
            
        except sqlite3.Error as e:
            return jsonify({'error': f'SQL error: {str(e)}'}), 400
            
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    
    table_name = init_credit_db()
    if table_name:
        print(f"Server starting... Database initialized with table: {table_name}")
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        print("Failed to initialize database. Check your CSV file and try again.")
    