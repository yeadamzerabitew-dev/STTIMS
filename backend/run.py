#!/usr/bin/env python3
"""STTIMS - Stable Server Runner"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STTIMS Server (Stable Mode)")
    print("=" * 60)
    print("📍 Server: http://127.0.0.1:5000")
    print("📍 Login: http://127.0.0.1:5000/pages/login.html")
    print("📍 Health: http://127.0.0.1:5000/health")
    print("=" * 60)
    print("🔧 Press Ctrl+C to stop")
    print("=" * 60)
    
    # Use production settings for stability
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True,
        processes=1
    )
