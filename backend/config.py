import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', True)
    
    # Database Configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'sttims_db')
    # Path to a CA certificate file, required by managed MySQL hosts that
    # enforce SSL (e.g. Aiven). Leave unset for a plain local MySQL install.
    DB_SSL_CA = os.environ.get('DB_SSL_CA', '')
    
    # SQLAlchemy Configuration
    _ssl_query = f"?ssl_ca={DB_SSL_CA}" if DB_SSL_CA else ""
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}{_ssl_query}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for debugging SQL queries
    
    # Session Configuration
    # SESSION_COOKIE_SECURE and SESSION_COOKIE_SAMESITE are set per-environment
    # below (DevelopmentConfig vs ProductionConfig) - see those classes for why.
    SESSION_COOKIE_HTTPONLY = True
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Allowed file extensions for uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour in seconds
    
    # Pagination
    DEFAULT_PAGE_SIZE = 10
    
    # Application Name
    APP_NAME = 'STTIMS'
    APP_VERSION = '1.0.0'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

    # Local dev: frontend and backend are both plain HTTP on 127.0.0.1, so
    # a Secure cookie would never be stored at all. 'Lax' is fine locally
    # since everything shares the same site (127.0.0.1).
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    # Deployed: frontend and backend live on different onrender.com
    # subdomains, which browsers treat as different *sites* (onrender.com
    # is on the public suffix list) - 'Lax' cookies are never sent on the
    # fetch() calls api.js makes, so this must be 'None' + Secure=True
    # (required together; satisfied since Render serves everything over HTTPS).
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'
    
    # In production, you should have a proper secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database credentials should be set in environment variables
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
