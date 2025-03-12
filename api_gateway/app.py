from flask import Flask, request, jsonify
from config.config import Config

app = Flask(__name__)

# Import routes
from routes.chatbot_routes import chatbot_bp

# Register blueprints
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "api-gateway"})

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
