from flask import Flask, request, jsonify
import service.chat
from service.decider import rag_decider_agent
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)