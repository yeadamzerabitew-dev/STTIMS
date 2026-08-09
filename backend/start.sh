#!/bin/bash

cd ~/Documents/sttims
source venv/bin/activate

# Kill any existing gunicorn processes
pkill -f gunicorn 2>/dev/null

echo "=========================================="
echo "🚀 STTIMS - Starting Production Server"
echo "=========================================="
echo "📍 Server: http://127.0.0.1:5000"
echo "📍 Login: http://127.0.0.1:5000/pages/login.html"
echo "📍 Health: http://127.0.0.1:5000/health"
echo "=========================================="
echo "🔧 Using Gunicorn (Production Ready)"
echo "=========================================="
echo "Press Ctrl+C to stop"
echo "=========================================="

# Start with gunicorn
gunicorn --bind 0.0.0.0:5000 \
         --workers 2 \
         --threads 4 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         app:app
