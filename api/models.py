from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # For serverless deployment, we'll use cloud AI services
        # These models represent what's available through external APIs
        models = [
            {
                'id': 'whisper-1', 
                'name': 'Whisper-1 (OpenAI)', 
                'description': 'OpenAI Whisper API - Best accuracy and speed'
            },
            {
                'id': 'base', 
                'name': 'Base', 
                'description': 'Balanced performance (fallback mode)'
            },
            {
                'id': 'small', 
                'name': 'Small', 
                'description': 'Better accuracy (fallback mode)'
            },
            {
                'id': 'medium', 
                'name': 'Medium', 
                'description': 'High accuracy (fallback mode)'
            }
        ]
        
        response = {
            'models': models,
            'default': 'whisper-1',
            'environment': 'vercel_serverless',
            'note': 'Using cloud AI services for serverless deployment'
        }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
