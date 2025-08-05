#!/usr/bin/env python3
"""
Social Media Automation Platform - Startup Script
This script helps you start both the backend and frontend servers.
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🚀 Social Media Automation Platform")
    print("=" * 60)
    print("Starting backend and frontend servers...")
    print()

def check_requirements():
    """Check if required software is installed."""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✅ Node.js found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is required but not found")
        return False
    
    # Check npm
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ npm found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm is required but not found")
        return False
    
    print("✅ All requirements met!")
    return True

def setup_backend():
    """Setup and start the backend server."""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
    
    # Install requirements
    print("Installing Python dependencies...")
    if os.name == "nt":  # Windows
        pip_cmd = str(venv_dir / "Scripts" / "pip")
    else:  # Unix/Linux/Mac
        pip_cmd = str(venv_dir / "bin" / "pip")
    
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], cwd=backend_dir)
    
    # Check if .env file exists
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  .env file not found. Please copy env.example to .env and configure it.")
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup and start the frontend server."""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install npm dependencies
    print("Installing npm dependencies...")
    subprocess.run(["npm", "install"], cwd=frontend_dir)
    
    print("✅ Frontend setup complete!")
    return True

def start_backend():
    """Start the backend server."""
    backend_dir = Path("backend")
    if os.name == "nt":  # Windows
        python_cmd = str(backend_dir / "venv" / "Scripts" / "python")
    else:  # Unix/Linux/Mac
        python_cmd = str(backend_dir / "venv" / "bin" / "python")
    
    print("🚀 Starting backend server...")
    subprocess.run([python_cmd, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"], cwd=backend_dir)

def start_frontend():
    """Start the frontend server."""
    frontend_dir = Path("frontend")
    print("🚀 Starting frontend server...")
    subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)

def main():
    print_banner()
    
    if not check_requirements():
        print("\n❌ Please install the missing requirements and try again.")
        sys.exit(1)
    
    # Setup both backend and frontend
    if not setup_backend():
        print("\n❌ Backend setup failed.")
        sys.exit(1)
    
    if not setup_frontend():
        print("\n❌ Frontend setup failed.")
        sys.exit(1)
    
    print("\n🎉 Setup complete! Starting servers...")
    print("\n📱 Frontend will be available at: http://localhost:3000")
    print("🔧 Backend API will be available at: http://localhost:8000")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all servers")
    
    # Start both servers in separate threads
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    
    try:
        backend_thread.start()
        time.sleep(2)  # Give backend a moment to start
        frontend_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        print("✅ Servers stopped. Goodbye!")

if __name__ == "__main__":
    main() 