from flask import Flask, request, jsonify
from core.conversation_manager import ConversationManager
from config.config import Config

app = Flask(__name__)
conversation_manager = ConversationManager()

@app.route('/conversation', methods=['POST'])
def start_conversation():
    """Start a new conversation session"""
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        
        # Create new conversation
        conversation_id = conversation_manager.create_conversation(user_id)
        
        # Get initial message
        initial_message = conversation_manager.get_welcome_message()
        
        return jsonify({
            "conversation_id": conversation_id,
            "message": initial_message
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST'])
def process_message():
    """Process a message in an existing conversation"""
    try:
        data = request.json
        conversation_id = data.get('conversation_id')
        text = data.get('text')
        
        if not conversation_id or not text:
            return jsonify({"error": "Missing conversation_id or text"}), 400
        
        # Process the message through conversation manager
        response = conversation_manager.process_message(conversation_id, text)
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation data"""
    try:
        conversation = conversation_manager.get_conversation(conversation_id)
        
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
            
        return jsonify(conversation), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
