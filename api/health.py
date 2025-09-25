from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

def handler(request):
    """Health check endpoint for Vercel"""
    
    if request.method == 'GET':
        return jsonify({
            'status': 'healthy',
            'message': 'ConvertAnything API is running on Vercel',
            'timestamp': datetime.now().isoformat(),
            'environment': 'production',
            'version': '1.0.0'
        })
    
    return jsonify({'error': 'Method not allowed'}), 405

# For local development
if __name__ == '__main__':
    app.run(debug=True)
