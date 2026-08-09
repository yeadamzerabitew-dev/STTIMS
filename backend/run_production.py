#!/usr/bin/env python3
"""STTIMS - Production Server (No Debug)"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STTIMS Production Server")
    print("=" * 60)
    print("📍 Server: http://127.0.0.1:5000")
    print("📍 Login: http://127.0.0.1:5000/pages/login.html")
    print("📍 Health: http://127.0.0.1:5000/health")
    print("=" * 60)
    print("🔧 Debug: DISABLED")
    print("🔧 Reloader: DISABLED")
    print("🔧 Threaded: YES")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Disable all debug features
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True,
        processes=1
    )
