#!/usr/bin/env python3
"""
Local development server for ConvertAnything
Runs both the Flask API backend and serves the frontend
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def run_backend():
    """Run the Flask API backend"""
    print("🚀 Starting Flask API backend on http://localhost:5000")
    try:
        subprocess.run([sys.executable, 'app.py'], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def run_frontend():
    """Run the frontend static server"""
    print("🌐 Starting frontend server on http://localhost:8000")
    try:
        subprocess.run([sys.executable, '-m', 'http.server', '8000'], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    missing_deps = []
    optional_missing = []
    
    # Core dependencies
    try:
        import flask
        print("✓ Flask is installed")
    except ImportError:
        missing_deps.append("flask")
    
    try:
        import flask_cors
        print("✓ Flask-CORS is installed")
    except ImportError:
        missing_deps.append("flask-cors")
    
    try:
        import whisper
        print("✓ OpenAI Whisper is installed")
    except ImportError:
        missing_deps.append("openai-whisper")
    
    try:
        import torch
        print("✓ PyTorch is installed")
    except ImportError:
        missing_deps.append("torch")
    
    # Optional dependencies
    try:
        from pyannote.audio import Pipeline
        print("✓ Pyannote Audio is installed")
    except ImportError:
        optional_missing.append("pyannote.audio")
        print("⚠ Pyannote Audio not found (speaker separation will use fallback)")
    
    try:
        import ffmpeg
        print("✓ FFmpeg-python is installed")
    except ImportError:
        optional_missing.append("ffmpeg-python")
        print("⚠ FFmpeg-python not found (audio duration detection may be less accurate)")
    
    if missing_deps:
        print(f"\n❌ Missing critical dependencies: {', '.join(missing_deps)}")
        print("Install with:")
        print(f"pip install {' '.join(missing_deps)}")
        print("\nOr install all dependencies:")
        print("pip install -r requirements-backend.txt")
        return False
    
    if optional_missing:
        print(f"\n⚠ Optional dependencies missing: {', '.join(optional_missing)}")
        print("For best experience, install with: pip install -r requirements-backend.txt")
    
    print("✅ All core dependencies are installed!")
    return True

def main():
    print("=" * 60)
    print("🎵 ConvertAnything - Local Development Server")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies before running.")
        return
    
    print("\nStarting both frontend and backend servers...")
    print("Frontend: http://localhost:8000")
    print("Backend API: http://localhost:5000")
    print("\nPress Ctrl+C to stop both servers")
    print("-" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:8000')
        print("🌐 Opening browser...")
    except:
        print("Could not open browser automatically")
        print("Please visit: http://localhost:8000")
    
    try:
        # Run frontend server in main thread
        run_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        print("Thank you for using ConvertAnything!")

if __name__ == '__main__':
    main()
