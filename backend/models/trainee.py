from datetime import datetime
from .base import db, BaseModel

class Trainee(BaseModel):
    __tablename__ = 'trainees'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    trainee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    trainee_code = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    
    # =============================================
    # PERSONAL INFORMATION
    # =============================================
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    
    # =============================================
    # CONTACT INFORMATION
    # =============================================
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    alternative_phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state_region = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), default='Ethiopia')
    
    # =============================================
    # EDUCATION AND OCCUPATION
    # =============================================
    educational_level = db.Column(db.Enum('High School', 'Diploma', 'BSc', 'MSc', 'PhD', 'Other'), nullable=False)
    occupation = db.Column(db.String(100), nullable=True)
    organization = db.Column(db.String(100), nullable=True)
    
    # =============================================
    # EMERGENCY CONTACT
    # =============================================
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(15), nullable=False)
    
    # =============================================
    # STATUS AND METADATA
    # =============================================
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('Active', 'Inactive', 'Suspended'), default='Active')
    profile_image = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. User relationship (1:1)
    user = db.relationship(
        'User', 
        back_populates='trainee_profile', 
        uselist=False, 
        foreign_keys='User.trainee_id'
    )
    
    # 2. Emergency Contacts relationship (1:M)
    emergency_contacts = db.relationship(
        'EmergencyContact', 
        back_populates='trainee', 
        lazy='dynamic'
    )
    
    # 3. Attendance Records relationship (1:M)
    attendance_records = db.relationship(
        'AttendanceRecord', 
        back_populates='trainee', 
        lazy='dynamic'
    )
    
    # 4. Trainee Results relationship (1:M)
    trainee_results = db.relationship(
        'TraineeResult', 
        back_populates='trainee', 
        lazy='dynamic'
    )
    
    # 5. Enrollments relationship (1:M)
    enrollments = db.relationship(
        'Enrollment', 
        back_populates='trainee', 
        lazy='dynamic'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def full_name(self):
        """Return the full name of the trainee"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = datetime.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    @property
    def is_active(self):
        return self.status == 'Active'
    
    @property
    def is_inactive(self):
        return self.status == 'Inactive'
    
    @property
    def is_suspended(self):
        return self.status == 'Suspended'
    
    @property
    def total_enrollments(self):
        """Get total number of enrollments"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.count()
        return 0
    
    @property
    def active_enrollments(self):
        """Get active enrollments count"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.filter_by(status='Active').count()
        return 0
    
    @property
    def enrolled_enrollments(self):
        """Get enrolled enrollments count"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.filter_by(status='Enrolled').count()
        return 0
    
    @property
    def completed_enrollments(self):
        """Get completed enrollments count"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.filter_by(status='Completed').count()
        return 0
    
    @property
    def dropped_enrollments(self):
        """Get dropped enrollments count"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.filter_by(status='Dropped').count()
        return 0
    
    @property
    def total_emergency_contacts(self):
        """Get total number of emergency contacts"""
        if hasattr(self, 'emergency_contacts'):
            return self.emergency_contacts.count()
        return 0
    
    @property
    def primary_emergency_contact(self):
        """Get the primary emergency contact"""
        if hasattr(self, 'emergency_contacts'):
            return self.emergency_contacts.filter_by(is_primary=True).first()
        return None
    
    @property
    def overall_attendance(self):
        """Calculate overall attendance percentage across all enrollments"""
        if hasattr(self, 'enrollments'):
            enrollments = self.enrollments.all()
            if enrollments:
                total_attendance = sum(e.attendance_percentage or 0 for e in enrollments)
                return round(total_attendance / len(enrollments), 2)
        return 0
    
    @property
    def overall_completion(self):
        """Calculate overall completion percentage across all enrollments"""
        if hasattr(self, 'enrollments'):
            enrollments = self.enrollments.all()
            if enrollments:
                total_completion = sum(e.completion_percentage or 0 for e in enrollments)
                return round(total_completion / len(enrollments), 2)
        return 0
    
    @property
    def latest_enrollment(self):
        """Get the most recent enrollment"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.order_by(
                db.desc(Enrollment.enrollment_date)
            ).first()
        return None
    
    @property
    def latest_course(self):
        """Get the most recent course"""
        enrollment = self.latest_enrollment
        if enrollment and enrollment.batch:
            return enrollment.batch.course
        return None
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Active': '✅ Active',
            'Inactive': '❌ Inactive',
            'Suspended': '⏸️ Suspended'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def gender_display(self):
        """Get display-friendly gender"""
        gender_map = {
            'Male': '👨 Male',
            'Female': '👩 Female',
            'Other': '👤 Other'
        }
        return gender_map.get(self.gender, self.gender)
    
    @property
    def educational_level_display(self):
        """Get display-friendly educational level"""
        level_map = {
            'High School': '📚 High School',
            'Diploma': '📜 Diploma',
            'BSc': '🎓 Bachelor',
            'MSc': '🎓 Master',
            'PhD': '🎓 PhD',
            'Other': '📖 Other'
        }
        return level_map.get(self.educational_level, self.educational_level)
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the trainee"""
        self.status = 'Active'
    
    def deactivate(self):
        """Deactivate the trainee"""
        self.status = 'Inactive'
    
    def suspend(self):
        """Suspend the trainee"""
        self.status = 'Suspended'
    
    def get_enrollments_by_status(self, status):
        """Get enrollments filtered by status"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.filter_by(status=status).all()
        return []
    
    def get_active_enrollments(self):
        """Get all active enrollments"""
        return self.get_enrollments_by_status('Active')
    
    def get_completed_enrollments(self):
        """Get all completed enrollments"""
        return self.get_enrollments_by_status('Completed')
    
    def get_dropped_enrollments(self):
        """Get all dropped enrollments"""
        return self.get_enrollments_by_status('Dropped')
    
    def get_primary_emergency_contact(self):
        """Get the primary emergency contact"""
        if hasattr(self, 'emergency_contacts'):
            return self.emergency_contacts.filter_by(is_primary=True).first()
        return None
    
    def get_latest_enrollment(self):
        """Get the most recent enrollment"""
        if hasattr(self, 'enrollments'):
            return self.enrollments.order_by(
                db.desc(Enrollment.enrollment_date)
            ).first()
        return None
    
    def get_attendance_summary(self):
        """Get attendance summary"""
        enrollments = self.enrollments.all()
        if not enrollments:
            return {
                'total': 0,
                'average_attendance': 0,
                'average_completion': 0
            }
        
        total_attendance = sum(e.attendance_percentage or 0 for e in enrollments)
        total_completion = sum(e.completion_percentage or 0 for e in enrollments)
        
        return {
            'total': len(enrollments),
            'average_attendance': round(total_attendance / len(enrollments), 2),
            'average_completion': round(total_completion / len(enrollments), 2)
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert trainee to dictionary"""
        return {
            'trainee_id': self.trainee_id,
            'trainee_code': self.trainee_code,
            'full_name': self.full_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'gender_display': self.gender_display,
            'email': self.email,
            'phone_number': self.phone_number,
            'alternative_phone': self.alternative_phone,
            'address': self.address,
            'city': self.city,
            'state_region': self.state_region,
            'country': self.country,
            'educational_level': self.educational_level,
            'educational_level_display': self.educational_level_display,
            'occupation': self.occupation,
            'organization': self.organization,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'status': self.status,
            'status_display': self.status_display,
            'is_active': self.is_active,
            'is_inactive': self.is_inactive,
            'is_suspended': self.is_suspended,
            'profile_image': self.profile_image,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_enrollments': self.total_enrollments,
            'active_enrollments': self.active_enrollments,
            'completed_enrollments': self.completed_enrollments,
            'dropped_enrollments': self.dropped_enrollments,
            'overall_attendance': self.overall_attendance,
            'overall_completion': self.overall_completion,
            'total_emergency_contacts': self.total_emergency_contacts,
            'primary_emergency_contact': self.primary_emergency_contact.to_dict() if self.primary_emergency_contact else None,
            'attendance_summary': self.get_attendance_summary()
        }
    
    def to_dict_minimal(self):
        """Convert trainee to minimal dictionary"""
        return {
            'trainee_id': self.trainee_id,
            'trainee_code': self.trainee_code,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<Trainee {self.trainee_code} - {self.full_name}>"
