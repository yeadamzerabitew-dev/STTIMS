from .base import db, BaseModel
from decimal import Decimal

class Course(BaseModel):
    __tablename__ = 'courses'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_title = db.Column(db.String(100), nullable=False)
    
    # =============================================
    # FOREIGN KEY
    # =============================================
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    
    # =============================================
    # DESCRIPTION
    # =============================================
    description = db.Column(db.Text, nullable=False)
    learning_objectives = db.Column(db.Text, nullable=True)
    prerequisites = db.Column(db.Text, nullable=True)
    
    # =============================================
    # DURATION
    # =============================================
    duration_hours = db.Column(db.Integer, nullable=False)
    duration_weeks = db.Column(db.Integer, nullable=True)
    
    # =============================================
    # FEE
    # =============================================
    fee_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    fee_currency = db.Column(db.String(3), default='ETB')
    
    # =============================================
    # REQUIREMENTS
    # =============================================
    min_age_requirement = db.Column(db.Integer, nullable=True)
    max_capacity = db.Column(db.Integer, nullable=False)
    
    # =============================================
    # LEVEL & CERTIFICATION
    # =============================================
    course_level = db.Column(db.Enum('Beginner', 'Intermediate', 'Advanced'), default='Beginner')
    certification_available = db.Column(db.Boolean, default=True)
    
    # =============================================
    # STATUS
    # =============================================
    status = db.Column(db.Enum('Active', 'Inactive', 'Archived'), default='Active')
    
    # =============================================
    # IMAGE
    # =============================================
    image_url = db.Column(db.String(255), nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Category relationship (M:1)
    category = db.relationship('Category', back_populates='courses')
    
    # 2. Batches relationship (1:M)
    batches = db.relationship('Batch', back_populates='course', lazy='dynamic')
    
    # 3. Certificate Settings relationship (1:M)
    certificate_settings = db.relationship('CertificateSetting', back_populates='course', lazy='dynamic')
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def category_name(self):
        """Get the category name"""
        if self.category:
            return self.category.category_name
        return None
    
    @property
    def category_code(self):
        """Get the category code"""
        if self.category:
            return self.category.category_code
        return None
    
    @property
    def is_active(self):
        return self.status == 'Active'
    
    @property
    def is_inactive(self):
        return self.status == 'Inactive'
    
    @property
    def is_archived(self):
        return self.status == 'Archived'
    
    @property
    def fee_display(self):
        """Get formatted fee"""
        return f"{self.fee_amount} {self.fee_currency}"
    
    @property
    def level_display(self):
        """Get display-friendly level"""
        level_map = {
            'Beginner': '🌱 Beginner',
            'Intermediate': '📈 Intermediate',
            'Advanced': '🚀 Advanced'
        }
        return level_map.get(self.course_level, self.course_level)
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Active': '✅ Active',
            'Inactive': '❌ Inactive',
            'Archived': '📦 Archived'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def total_batches(self):
        """Get total number of batches"""
        if hasattr(self, 'batches'):
            return self.batches.count()
        return 0
    
    @property
    def active_batches(self):
        """Get number of active batches"""
        if hasattr(self, 'batches'):
            return self.batches.filter_by(status='Ongoing').count()
        return 0
    
    @property
    def upcoming_batches(self):
        """Get number of upcoming batches"""
        if hasattr(self, 'batches'):
            return self.batches.filter_by(status='Upcoming').count()
        return 0
    
    @property
    def completed_batches(self):
        """Get number of completed batches"""
        if hasattr(self, 'batches'):
            return self.batches.filter_by(status='Completed').count()
        return 0
    
    @property
    def total_enrollments(self):
        """Get total enrollments across all batches"""
        total = 0
        if hasattr(self, 'batches'):
            for batch in self.batches.all():
                total += batch.enrollments.count()
        return total
    
    @property
    def active_enrollments(self):
        """Get active enrollments across all batches"""
        total = 0
        if hasattr(self, 'batches'):
            for batch in self.batches.all():
                total += batch.enrollments.filter_by(status='Active').count()
        return total
    
    @property
    def completed_enrollments(self):
        """Get completed enrollments across all batches"""
        total = 0
        if hasattr(self, 'batches'):
            for batch in self.batches.all():
                total += batch.enrollments.filter_by(status='Completed').count()
        return total
    
    @property
    def total_revenue(self):
        """Get total revenue across all batches"""
        total = Decimal('0.00')
        if hasattr(self, 'batches'):
            for batch in self.batches.all():
                for enrollment in batch.enrollments.all():
                    if enrollment.payment_amount:
                        total += enrollment.payment_amount
        return total
    
    @property
    def total_capacity(self):
        """Get total capacity across all batches"""
        total = 0
        if hasattr(self, 'batches'):
            for batch in self.batches.all():
                total += batch.max_capacity
        return total
    
    @property
    def average_attendance(self):
        """Get average attendance percentage across all active enrollments"""
        if hasattr(self, 'batches'):
            enrollments = []
            for batch in self.batches.all():
                enrollments.extend(batch.enrollments.filter_by(status='Active').all())
            if enrollments:
                total = sum(e.attendance_percentage or 0 for e in enrollments)
                return round(total / len(enrollments), 2)
        return 0
    
    @property
    def average_completion(self):
        """Get average completion percentage across all active enrollments"""
        if hasattr(self, 'batches'):
            enrollments = []
            for batch in self.batches.all():
                enrollments.extend(batch.enrollments.filter_by(status='Active').all())
            if enrollments:
                total = sum(e.completion_percentage or 0 for e in enrollments)
                return round(total / len(enrollments), 2)
        return 0
    
    @property
    def has_certification(self):
        return self.certification_available
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the course"""
        self.status = 'Active'
    
    def deactivate(self):
        """Deactivate the course"""
        self.status = 'Inactive'
    
    def archive(self):
        """Archive the course"""
        self.status = 'Archived'
    
    def get_certificate_templates(self):
        """Get all certificate templates for this course"""
        if hasattr(self, 'certificate_settings'):
            return self.certificate_settings.filter_by(status='Active').all()
        return []
    
    def get_default_certificate_template(self):
        """Get default certificate template for this course"""
        if hasattr(self, 'certificate_settings'):
            return self.certificate_settings.filter_by(is_default=True).first()
        return None
    
    def get_batches_by_status(self, status):
        """Get batches filtered by status"""
        if hasattr(self, 'batches'):
            return self.batches.filter_by(status=status).all()
        return []
    
    def get_upcoming_batches(self):
        """Get upcoming batches"""
        return self.get_batches_by_status('Upcoming')
    
    def get_ongoing_batches(self):
        """Get ongoing batches"""
        return self.get_batches_by_status('Ongoing')
    
    def get_completed_batches(self):
        """Get completed batches"""
        return self.get_batches_by_status('Completed')
    
    def get_statistics(self):
        """Get course statistics"""
        return {
            'total_batches': self.total_batches,
            'active_batches': self.active_batches,
            'upcoming_batches': self.upcoming_batches,
            'completed_batches': self.completed_batches,
            'total_enrollments': self.total_enrollments,
            'active_enrollments': self.active_enrollments,
            'completed_enrollments': self.completed_enrollments,
            'total_revenue': float(self.total_revenue),
            'total_capacity': self.total_capacity,
            'average_attendance': self.average_attendance,
            'average_completion': self.average_completion
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert course to dictionary"""
        return {
            'course_id': self.course_id,
            'course_code': self.course_code,
            'course_title': self.course_title,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'category_code': self.category_code,
            'description': self.description,
            'learning_objectives': self.learning_objectives,
            'prerequisites': self.prerequisites,
            'duration_hours': self.duration_hours,
            'duration_weeks': self.duration_weeks,
            'fee_amount': float(self.fee_amount),
            'fee_currency': self.fee_currency,
            'fee_display': self.fee_display,
            'min_age_requirement': self.min_age_requirement,
            'max_capacity': self.max_capacity,
            'course_level': self.course_level,
            'level_display': self.level_display,
            'certification_available': self.certification_available,
            'has_certification': self.has_certification,
            'status': self.status,
            'status_display': self.status_display,
            'is_active': self.is_active,
            'is_inactive': self.is_inactive,
            'is_archived': self.is_archived,
            'image_url': self.image_url,
            'statistics': self.get_statistics(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert course to minimal dictionary"""
        return {
            'course_id': self.course_id,
            'course_code': self.course_code,
            'course_title': self.course_title,
            'category_name': self.category_name,
            'fee_amount': float(self.fee_amount),
            'course_level': self.course_level,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<Course {self.course_code} - {self.course_title}>"
