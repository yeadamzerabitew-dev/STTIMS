from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import db, BaseModel

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # AUTHENTICATION FIELDS
    # =============================================
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # =============================================
    # ROLE & RELATIONSHIP FIELDS
    # =============================================
    role = db.Column(db.Enum('Admin', 'Instructor', 'Trainee', 'Manager'), nullable=False)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'), nullable=True)
    
    # =============================================
    # STATUS & METADATA
    # =============================================
    status = db.Column(db.Enum('Active', 'Inactive', 'Locked'), default='Active')
    last_login = db.Column(db.DateTime, nullable=True)
    login_attempts = db.Column(db.Integer, default=0)
    
    # =============================================
    # RELATIONSHIPS
    # =============================================
    
    # 1. Trainee Profile relationship (1:1)
    trainee_profile = db.relationship(
        'Trainee', 
        back_populates='user', 
        uselist=False, 
        foreign_keys='User.trainee_id'
    )
    
    # 2. Instructor Profile relationship (1:1)
    instructor_profile = db.relationship(
        'Instructor', 
        back_populates='user', 
        uselist=False, 
        foreign_keys='User.instructor_id'
    )
    
    # 3. System Logs relationship (1:M)
    logs = db.relationship(
        'SystemLog', 
        back_populates='user', 
        lazy='dynamic'
    )
    
    # 4. Notifications relationship (1:M)
    notifications = db.relationship(
        'Notification', 
        back_populates='user', 
        lazy='dynamic'
    )
    
    # 5. Approved Certificates relationship (1:M)
    approved_certificates = db.relationship(
        'Certificate', 
        back_populates='approved_by_user', 
        foreign_keys='Certificate.approved_by'
    )
    
    # 6. Created Assessments relationship (1:M)
    created_assessments = db.relationship(
        'Assessment', 
        back_populates='creator', 
        foreign_keys='Assessment.created_by'
    )
    
    # 7. Created Course Assignments relationship (1:M)
    created_assignments = db.relationship(
        'CourseAssignment', 
        back_populates='creator', 
        foreign_keys='CourseAssignment.created_by'
    )
    
    # 8. Recorded Attendance relationship (1:M)
    recorded_attendance = db.relationship(
        'AttendanceRecord', 
        back_populates='recorder', 
        foreign_keys='AttendanceRecord.recorded_by'
    )
    
    # 9. Recorded Results relationship (1:M)
    recorded_results = db.relationship(
        'TraineeResult', 
        back_populates='recorder', 
        foreign_keys='TraineeResult.recorded_by'
    )
    
    # =============================================
    # FLASK-LOGIN REQUIRED METHODS
    # =============================================
    
    def get_id(self):
        """Flask-Login requires this method to get the user ID."""
        return str(self.user_id)
    
    def is_authenticated(self):
        """Flask-Login: Check if user is authenticated"""
        return True
    
    def is_anonymous(self):
        """Flask-Login: Check if user is anonymous"""
        return False
    
    # =============================================
    # PASSWORD METHODS
    # =============================================
    
    def set_password(self, password):
        """Hash and set the password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.
        Guards against NULL or malformed hashes (e.g. leftover
        placeholder seed data) so a bad row can't crash login
        with a 500 - it just fails the check instead.
        """
        if not self.password_hash:
            return False
        try:
            return check_password_hash(self.password_hash, password)
        except (ValueError, TypeError):
            return False
    
    # =============================================
    # ROLE CHECK METHODS
    # =============================================
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_instructor(self):
        return self.role == 'Instructor'
    
    def is_trainee(self):
        return self.role == 'Trainee'
    
    def is_manager(self):
        return self.role == 'Manager'
    
    def has_role(self, role):
        return self.role == role
    
    def has_any_role(self, roles):
        return self.role in roles
    
    def get_role_display(self):
        return self.role
    
    # =============================================
    # STATUS METHODS
    # =============================================
    
    def is_active(self):
        """Check if user account is active"""
        return self.status == 'Active'
    
    def is_locked(self):
        return self.status == 'Locked'
    
    def is_inactive(self):
        return self.status == 'Inactive'
    
    def activate(self):
        self.status = 'Active'
    
    def deactivate(self):
        self.status = 'Inactive'
    
    def lock(self):
        self.status = 'Locked'
    
    def unlock(self):
        self.status = 'Active'
        self.login_attempts = 0
    
    # =============================================
    # LOGIN ATTEMPTS METHODS
    # =============================================
    
    def increment_login_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.status = 'Locked'
    
    def reset_login_attempts(self):
        self.login_attempts = 0
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
    
    def get_remaining_attempts(self):
        return max(0, 5 - self.login_attempts)
    
    # =============================================
    # TRAINEE/INSTRUCTOR ACCESS METHODS
    # =============================================
    
    def get_trainee(self):
        if self.is_trainee() and self.trainee_id:
            return Trainee.query.get(self.trainee_id)
        return None
    
    def get_instructor(self):
        if self.is_instructor() and self.instructor_id:
            return Instructor.query.get(self.instructor_id)
        return None
    
    def get_profile(self):
        if self.is_trainee():
            return self.get_trainee()
        elif self.is_instructor():
            return self.get_instructor()
        return None
    
    # =============================================
    # PERMISSION METHODS
    # =============================================
    
    def can_access_module(self, module):
        permissions = {
            'admin': ['Admin'],
            'dashboard': ['Admin', 'Manager', 'Instructor', 'Trainee'],
            'users': ['Admin'],
            'trainees': ['Admin', 'Manager', 'Instructor'],
            'instructors': ['Admin', 'Manager'],
            'categories': ['Admin', 'Manager'],
            'courses': ['Admin', 'Manager', 'Instructor'],
            'batches': ['Admin', 'Manager', 'Instructor'],
            'enrollments': ['Admin', 'Manager', 'Instructor'],
            'sessions': ['Admin', 'Manager', 'Instructor'],
            'attendance': ['Admin', 'Manager', 'Instructor'],
            'assessments': ['Admin', 'Manager', 'Instructor'],
            'results': ['Admin', 'Manager', 'Instructor'],
            'certificates': ['Admin', 'Manager', 'Instructor', 'Trainee'],
            'reports': ['Admin', 'Manager'],
            'settings': ['Admin', 'Manager'],
            'profile': ['Admin', 'Manager', 'Instructor', 'Trainee']
        }
        allowed_roles = permissions.get(module, [])
        return self.role in allowed_roles
    
    def can_manage_users(self):
        return self.role in ['Admin', 'Manager']
    
    def can_manage_trainees(self):
        return self.role in ['Admin', 'Manager', 'Instructor']
    
    def can_manage_courses(self):
        return self.role in ['Admin', 'Manager', 'Instructor']
    
    def can_generate_reports(self):
        return self.role in ['Admin', 'Manager']
    
    def can_issue_certificates(self):
        return self.role in ['Admin', 'Manager', 'Instructor']
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'role_display': self.get_role_display(),
            'status': self.status,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_attempts': self.login_attempts,
            'remaining_attempts': self.get_remaining_attempts(),
            'trainee_id': self.trainee_id,
            'instructor_id': self.instructor_id,
            'is_admin': self.is_admin(),
            'is_instructor': self.is_instructor(),
            'is_trainee': self.is_trainee(),
            'is_manager': self.is_manager(),
            'is_active': self.is_active(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status
        }
    
    def to_dict_public(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'role_display': self.get_role_display(),
            'status': self.status,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
    
    def __str__(self):
        return self.username
