#!/usr/bin/env python3
"""STTIMS - Stable Server with Optimized Settings"""

import os
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STTIMS Server (Optimized Stable Mode)")
    print("=" * 60)
    print("📍 Server: http://127.0.0.1:5000")
    print("📍 Login: http://127.0.0.1:5000/pages/login.html")
    print("📍 Health: http://127.0.0.1:5000/health")
    print("=" * 60)
    print("🔧 Press Ctrl+C to stop")
    print("=" * 60)
    
    # Optimized settings for stability
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=False,  # Disable threading to reduce resource usage
        processes=1,
        request_handler=None
    )
