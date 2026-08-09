# =============================================
# STTIMS - Short-Term Training Institution 
# Management System
# Backend Application Entry Point
# Version: 1.0.0
# =============================================

import os
import json
import click
from flask import Flask, jsonify, request, send_from_directory
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import text
from time import time
from collections import defaultdict

# =============================================
# IMPORT db FROM models (SINGLE SOURCE OF TRUTH)
# =============================================
from models import db

# =============================================
# Load Environment Variables
# =============================================
load_dotenv()

# =============================================
# Initialize extensions at module level
# =============================================
migrate = Migrate()
login_manager = LoginManager()
cors = CORS()

# =============================================
# Rate Limiting for Health Checks
# =============================================
health_check_tracker = defaultdict(list)
HEALTH_CHECK_LIMIT = 10  # Max 10 health checks per minute
HEALTH_CHECK_WINDOW = 60  # 60 seconds window


def create_app(config_class=None):
    """
    Application Factory Function
    """
    
    # Create Flask app
    app = Flask(__name__)
    
    # Set secret key
    app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-this-in-production')
    
    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # =============================================
    # CRITICAL: Initialize db with the app
    # =============================================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    
    # Import models (needed for migrations)
    from models import (
        User, Trainee, Instructor, Course, Category, Batch,
        Enrollment, ClassSession, AttendanceRecord, Assessment, TraineeResult,
        Certificate, CertificateSetting, CourseAssignment, GradeScale,
        EmergencyContact, InstructorSpecialization, SystemLog, Notification,
        Setting
    )
    
    # Import and register blueprints
    from routes import (
        auth_bp, user_bp, trainee_bp, instructor_bp, category_bp,
        course_bp, batch_bp, enrollment_bp, session_bp, attendance_bp,
        assessment_bp, result_bp, certificate_bp, report_bp, dashboard_bp,
        settings_bp
    )
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(trainee_bp, url_prefix='/api/trainees')
    app.register_blueprint(instructor_bp, url_prefix='/api/instructors')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(course_bp, url_prefix='/api/courses')
    app.register_blueprint(batch_bp, url_prefix='/api/batches')
    app.register_blueprint(enrollment_bp, url_prefix='/api/enrollments')
    app.register_blueprint(session_bp, url_prefix='/api/sessions')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(assessment_bp, url_prefix='/api/assessments')
    app.register_blueprint(result_bp, url_prefix='/api/results')
    app.register_blueprint(certificate_bp, url_prefix='/api/certificates')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    
    # =============================================
    # Normalize API Responses
    # -----------------------------------------------
    # The frontend always reads a response's payload from a `data` key
    # and its page count from `total_pages`, but controllers return the
    # payload under an entity-specific key (`trainee`, `user`, `batch`,
    # `attendance`, `results`, etc.) and expose the page count as
    # `pages`. This hook aliases the correct key onto `data`, and
    # `pages` onto `total_pages`, based on the request URL - purely
    # additive, never overwrites an existing key.
    # =============================================
    MODULE_RESPONSE_KEYS = {
        'users':        ('users', 'user'),
        'trainees':     ('trainees', 'trainee'),
        'instructors':  ('instructors', 'instructor'),
        'categories':   ('categories', 'category'),
        'courses':      ('courses', 'course'),
        'batches':      ('batches', 'batch'),
        'enrollments':  ('enrollments', 'enrollment'),
        'sessions':     ('sessions', 'session'),
        'attendance':   ('attendance', 'attendance'),
        'assessments':  ('assessments', 'assessment'),
        'results':      ('results', 'result'),
        'certificates': ('certificates', 'certificate'),
    }

    @app.after_request
    def normalize_api_response(response):
        """Alias each module's real response key(s) onto 'data', and 'pages' onto 'total_pages'."""
        try:
            if not request.path.startswith('/api/'):
                return response
            if response.mimetype != 'application/json':
                return response

            payload = response.get_json(silent=True)
            if not isinstance(payload, dict):
                return response

            segments = [s for s in request.path.split('/') if s]
            module = segments[1] if len(segments) > 1 else None
            changed = False

            if 'data' not in payload and module in MODULE_RESPONSE_KEYS:
                list_key, single_key = MODULE_RESPONSE_KEYS[module]
                if list_key in payload:
                    payload['data'] = payload[list_key]
                    changed = True
                elif single_key in payload:
                    payload['data'] = payload[single_key]
                    changed = True

            if 'pages' in payload and 'total_pages' not in payload:
                payload['total_pages'] = payload['pages']
                changed = True

            if changed:
                response.set_data(json.dumps(payload))

            return response
        except Exception:
            return response

    # =============================================
    # CORS Headers (Manual fallback)
    # =============================================
    @app.after_request
    def add_cors_headers(response):
        """Add CORS headers to all responses"""
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response
    
    # =============================================
    # Handle OPTIONS requests for CORS preflight
    # =============================================
    @app.before_request
    def handle_preflight():
        """Handle CORS preflight requests"""
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
    
    # Security Headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Error Handlers
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(503)
    def service_unavailable_error(error):
        return jsonify({'error': 'Service unavailable'}), 503
    
    # =============================================
    # Health Check with Rate Limiting
    # =============================================
    @app.route('/health', methods=['GET', 'OPTIONS'])
    def health_check():
        """Health check endpoint with rate limiting to prevent excessive requests"""
        # Rate limiting
        client_ip = request.remote_addr
        now = time()
        tracker = health_check_tracker[client_ip]
        
        # Remove old entries
        tracker[:] = [t for t in tracker if now - t < HEALTH_CHECK_WINDOW]
        
        if len(tracker) >= HEALTH_CHECK_LIMIT:
            return jsonify({
                'error': 'Too many health check requests',
                'retry_after': HEALTH_CHECK_WINDOW
            }), 429
        
        tracker.append(now)
        
        try:
            db.session.execute(text('SELECT 1'))
            db_status = 'healthy'
        except Exception as e:
            db_status = 'unhealthy'
            app.logger.error(f'Database health check failed: {e}')
        
        return jsonify({
            'status': 'healthy' if db_status == 'healthy' else 'degraded',
            'app': 'STTIMS',
            'version': '1.0.0',
            'database': db_status,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    # =============================================
    # API Home Route
    # =============================================
    @app.route('/api', methods=['GET'])
    def api_index():
        return jsonify({
            'message': 'Welcome to STTIMS API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'auth': '/api/auth/*',
                'users': '/api/users/*',
                'trainees': '/api/trainees/*',
                'instructors': '/api/instructors/*',
                'categories': '/api/categories/*',
                'courses': '/api/courses/*',
                'batches': '/api/batches/*',
                'enrollments': '/api/enrollments/*',
                'sessions': '/api/sessions/*',
                'attendance': '/api/attendance/*',
                'assessments': '/api/assessments/*',
                'results': '/api/results/*',
                'certificates': '/api/certificates/*',
                'reports': '/api/reports/*',
                'dashboard': '/api/dashboard/*',
                'settings': '/api/settings/*'
            }
        }), 200
    
    # =============================================
    # SERVE FRONTEND FROM FLASK
    # =============================================
    
    # Get the frontend directory
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sttims-frontend')
    
    # If the above doesn't work, try this alternative:
    if not os.path.exists(frontend_dir):
        frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'sttims-frontend')
    
    if frontend_dir and os.path.exists(frontend_dir):
        @app.route('/')
        def serve_index():
            """Serve the main index page"""
            return send_from_directory(frontend_dir, 'index.html')
        
        @app.route('/pages/<path:filename>')
        def serve_pages(filename):
            """Serve frontend pages"""
            return send_from_directory(os.path.join(frontend_dir, 'pages'), filename)
        
        @app.route('/js/<path:filename>')
        def serve_js(filename):
            """Serve frontend JavaScript files"""
            return send_from_directory(os.path.join(frontend_dir, 'js'), filename)
        
        @app.route('/css/<path:filename>')
        def serve_css(filename):
            """Serve frontend CSS files"""
            return send_from_directory(os.path.join(frontend_dir, 'css'), filename)
        
        @app.route('/images/<path:filename>')
        def serve_images(filename):
            """Serve frontend images"""
            return send_from_directory(os.path.join(frontend_dir, 'images'), filename)
        
        @app.route('/assets/<path:filename>')
        def serve_assets(filename):
            """Serve frontend assets"""
            return send_from_directory(os.path.join(frontend_dir, 'assets'), filename)
        
        # Catch-all route for frontend - must be last
        @app.route('/<path:path>')
        def serve_frontend(path):
            """Serve any frontend file or fallback to index.html"""
            # If it's an API call, let it pass
            if path.startswith('api/') or path.startswith('health'):
                return jsonify({'error': 'Not found'}), 404
            
            # Try to serve the file
            for folder in ['pages', 'js', 'css', 'images', 'assets']:
                file_path = os.path.join(frontend_dir, folder, path)
                if os.path.exists(file_path):
                    return send_from_directory(os.path.join(frontend_dir, folder), path)
            
            # If file not found, serve index.html for SPA routing
            if os.path.exists(os.path.join(frontend_dir, 'index.html')):
                return send_from_directory(frontend_dir, 'index.html')
            
            return jsonify({'error': 'File not found'}), 404
        
        app.logger.info(f'📁 Frontend directory served from: {frontend_dir}')
    else:
        app.logger.warning('⚠️ Frontend directory not found. Static files will not be served.')
    
    return app


# =============================================
# Create app instance
# =============================================
app = create_app()


# =============================================
# User loader for Flask-Login
# =============================================
@login_manager.user_loader
def load_user(user_id):
    from models import User
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError):
        return None


# =============================================
# CLI Commands
# =============================================

@app.cli.command('create-admin')
def create_admin_command():
    """Create an admin user"""
    print("\n" + "=" * 50)
    print("🔐 Create Admin User")
    print("=" * 50 + "\n")
    
    username = input('Enter admin username: ')
    email = input('Enter admin email: ')
    password = input('Enter admin password: ')
    
    from models import User
    
    if User.query.filter_by(username=username).first():
        click.echo(f'\n❌ Username "{username}" already exists!')
        return
    
    if User.query.filter_by(email=email).first():
        click.echo(f'\n❌ Email "{email}" already exists!')
        return
    
    user = User(
        username=username,
        email=email,
        role='Admin',
        status='Active'
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    click.echo(f'\n✅ Admin user "{username}" created successfully!')


@app.cli.command('list-users')
def list_users_command():
    """List all users"""
    from models import User
    
    print("\n" + "=" * 70)
    print("📋 List of Users")
    print("=" * 70 + "\n")
    
    users = User.query.all()
    
    if not users:
        print("No users found.")
        return
    
    print(f"{'ID':<6} {'Username':<20} {'Email':<30} {'Role':<12} {'Status':<10}")
    print("-" * 70)
    
    for user in users:
        print(f"{user.user_id:<6} {user.username:<20} {user.email:<30} {user.role:<12} {user.status:<10}")
    
    print("-" * 70)
    print(f"\nTotal users: {len(users)}")


@app.cli.command('create-test-users')
def create_test_users_command():
    """Create test users"""
    from models import User
    
    print("\n" + "=" * 50)
    print("🧪 Creating Test Users")
    print("=" * 50 + "\n")
    
    existing_users = User.query.all()
    if existing_users:
        print("⚠️  Users already exist in database!")
        return
    
    test_users = [
        {'username': 'admin', 'email': 'admin@sttims.com', 'role': 'Admin', 'password': 'Admin123!'},
        {'username': 'manager', 'email': 'manager@sttims.com', 'role': 'Manager', 'password': 'Manager123!'},
        {'username': 'instructor', 'email': 'instructor@sttims.com', 'role': 'Instructor', 'password': 'Instructor123!'},
        {'username': 'trainee', 'email': 'trainee@sttims.com', 'role': 'Trainee', 'password': 'Trainee123!'}
    ]
    
    for user_data in test_users:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            role=user_data['role'],
            status='Active'
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        print(f"✅ Created user: {user_data['username']}")
    
    db.session.commit()
    
    print("\n" + "=" * 50)
    print("✅ All test users created successfully!")
    print("=" * 50)
    print("\n📋 Test Credentials:")
    print("   Admin:      admin / Admin123!")
    print("   Manager:    manager / Manager123!")
    print("   Instructor: instructor / Instructor123!")
    print("   Trainee:    trainee / Trainee123!")
    print("=" * 50)


@app.cli.command('drop-tables')
def drop_tables_command():
    """Drop all tables (CAUTION: This will delete all data!)"""
    confirm = input("⚠️  This will delete ALL data. Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        db.drop_all()
        print("✅ All tables dropped!")
    else:
        print("❌ Operation cancelled.")


# =============================================
# Application Entry Point
# =============================================
if __name__ == '__main__':
    # Use debug=False for stability, True for development
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("🚀 STTIMS Backend Server Starting...")
    print("=" * 60)
    print(f"📍 API Server: http://127.0.0.1:5000")
    print(f"📍 Health Check: http://127.0.0.1:5000/health")
    print(f"📍 Frontend: http://127.0.0.1:5000/pages/login.html")
    print(f"📍 API Endpoints: http://127.0.0.1:5000/api")
    print("=" * 60)
    print(f"🔧 Debug Mode: {DEBUG_MODE}")
    print("📋 CORS Configuration:")
    print("   - Allow-Origin: *")
    print("   - Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS")
    print("   - Allow-Headers: Content-Type, Authorization")
    print("=" * 60)
    print("📋 Test Credentials:")
    print("   Admin:      admin / Admin123!")
    print("   Manager:    manager / Manager123!")
    print("   Instructor: instructor / Instructor123!")
    print("   Trainee:    trainee / Trainee123!")
    print("=" * 60)
    print("Press CTRL+C to quit")
    print("=" * 60)
    
    # Run with stability optimizations
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=DEBUG_MODE,
        use_reloader=DEBUG_MODE,  # Only use reloader in debug mode
        threaded=True if DEBUG_MODE else False,  # Disable threading for stability in production
        processes=1
    )

# Add this route to test data
@app.route('/api/test-data')
def test_data():
    from models import User, Trainee, Instructor, Course, Category, Batch, Enrollment
    
    data = {
        'users': User.query.count(),
        'trainees': Trainee.query.count(),
        'instructors': Instructor.query.count(),
        'courses': Course.query.count(),
        'categories': Category.query.count(),
        'batches': Batch.query.count(),
        'enrollments': Enrollment.query.count(),
    }
    
    return {'status': 'success', 'data': data}
