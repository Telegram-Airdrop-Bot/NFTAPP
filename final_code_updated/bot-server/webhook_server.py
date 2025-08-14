#!/usr/bin/env python3
"""
Webhook Server - Handles verification callbacks from API server
"""

import os
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Webhook data storage
WEBHOOK_DATA_FILE = "webhook_data.json"

def save_webhook_data(data):
    """Save webhook data to file for bot to process"""
    try:
        # Add timestamp
        data['timestamp'] = time.time()
        
        # Save to file
        with open(WEBHOOK_DATA_FILE, 'w') as f:
            json.dump(data, f)
        
        print(f"✅ Webhook data saved: {data}")
        return True
    except Exception as e:
        print(f"❌ Error saving webhook data: {e}")
        return False

@app.route('/verify_callback', methods=['POST'])
def verify_callback():
    """Receive verification results from API server"""
    try:
        data = request.json
        print(f"🔍 Webhook callback received: {data}")
        
        # Save data for bot to process
        if save_webhook_data(data):
            return jsonify({"status": "success", "message": "Webhook data saved"})
        else:
            return jsonify({"status": "error", "message": "Failed to save webhook data"}), 500
        
    except Exception as e:
        print(f"❌ Error in webhook callback: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "webhook-server"})

@app.route('/webhook_data', methods=['GET'])
def get_webhook_data():
    """Get latest webhook data (for bot to read)"""
    try:
        if os.path.exists(WEBHOOK_DATA_FILE):
            with open(WEBHOOK_DATA_FILE, 'r') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({"status": "no_data"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/clear_webhook_data', methods=['POST'])
def clear_webhook_data():
    """Clear webhook data (for bot to call after processing)"""
    try:
        if os.path.exists(WEBHOOK_DATA_FILE):
            os.remove(WEBHOOK_DATA_FILE)
            print("✅ Webhook data cleared")
        return jsonify({"status": "success", "message": "Webhook data cleared"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"🌐 Webhook server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 