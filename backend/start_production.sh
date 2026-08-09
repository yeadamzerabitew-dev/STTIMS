#!/bin/bash

cd ~/Documents/sttims
source venv/bin/activate

# Kill any existing processes
pkill -f gunicorn 2>/dev/null
pkill -f "python.*app" 2>/dev/null
sleep 2

echo "=========================================="
echo "🚀 STTIMS Production Server"
echo "=========================================="
echo "📍 Server: http://127.0.0.1:5000"
echo "📍 Login: http://127.0.0.1:5000/pages/login.html"
echo "📍 Health: http://127.0.0.1:5000/health"
echo "=========================================="
echo "🔧 Using Gunicorn (Production Ready)"
echo "=========================================="
echo "Press Ctrl+C to stop"
echo "=========================================="

# Start with Gunicorn
gunicorn --config gunicorn.conf.py app:app
