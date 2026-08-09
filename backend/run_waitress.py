#!/usr/bin/env python3
"""STTIMS - Waitress Production Server"""

import os
from waitress import serve
from app import app

print("=" * 60)
print("🚀 STTIMS Server (Waitress - Production)")
print("=" * 60)
print("📍 Server: http://127.0.0.1:5000")
print("📍 Login: http://127.0.0.1:5000/pages/login.html")
print("📍 Health: http://127.0.0.1:5000/health")
print("=" * 60)
print("🔧 Using Waitress (Production Ready)")
print("=" * 60)
print("Press Ctrl+C to stop")
print("=" * 60)

serve(app, host='127.0.0.1', port=5000, threads=4)
