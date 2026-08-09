#!/bin/bash

echo "=========================================="
echo "🔧 Setting up STTIMS Stable Server"
echo "=========================================="

cd ~/Documents/sttims
source venv/bin/activate

# Kill existing processes
pkill -f gunicorn 2>/dev/null
pkill -f "python.*app" 2>/dev/null
sudo fuser -k 5000/tcp 2>/dev/null
sleep 2

# Install gunicorn if not installed
if ! command -v gunicorn &> /dev/null; then
    echo "📦 Installing gunicorn..."
    pip install gunicorn
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the server:"
echo "   cd ~/Documents/sttims"
echo "   source venv/bin/activate"
echo "   ./start_production.sh"
echo ""
echo "📍 Access: http://127.0.0.1:5000/pages/login.html"
echo "🔑 Login: admin / Admin123!"
