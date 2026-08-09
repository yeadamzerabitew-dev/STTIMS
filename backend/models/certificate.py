from .base import db, BaseModel
from datetime import datetime, date, timedelta

class Certificate(BaseModel):
    __tablename__ = 'certificates'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    certificate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # CERTIFICATE IDENTIFICATION
    # =============================================
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    verification_token = db.Column(db.String(100), unique=True, nullable=False)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('certificate_settings.setting_id'), nullable=True)
    
    # =============================================
    # DATES
    # =============================================
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    
    # =============================================
    # CERTIFICATE DATA
    # =============================================
    certificate_url = db.Column(db.String(255), nullable=True)
    verification_qr = db.Column(db.String(255), nullable=True)
    issue_reason = db.Column(db.String(100), default='Course Completion')
    signature_image = db.Column(db.String(255), nullable=True)
    
    # =============================================
    # STATUS
    # =============================================
    status = db.Column(db.Enum('Issued', 'Revoked', 'Expired', 'Pending'), default='Pending')
    
    # =============================================
    # NOTES
    # =============================================
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Enrollment relationship (1:1)
    enrollment = db.relationship(
        'Enrollment', 
        back_populates='certificate',
        uselist=False
    )
    
    # 2. Template relationship (M:1)
    template = db.relationship(
        'CertificateSetting', 
        back_populates='certificates'
    )
    
    # 3. Approved By User relationship (M:1)
    approved_by_user = db.relationship(
        'User', 
        back_populates='approved_certificates',
        foreign_keys='Certificate.approved_by'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def is_valid(self):
        """Check if certificate is valid and not expired"""
        if self.status != 'Issued':
            return False
        if self.expiry_date and self.expiry_date < date.today():
            return False
        return True
    
    @property
    def is_expired(self):
        """Check if certificate has expired"""
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False
    
    @property
    def is_pending(self):
        return self.status == 'Pending'
    
    @property
    def is_issued(self):
        return self.status == 'Issued'
    
    @property
    def is_revoked(self):
        return self.status == 'Revoked'
    
    @property
    def days_until_expiry(self):
        """Get days until certificate expires"""
        if self.expiry_date:
            if self.is_valid:
                return (self.expiry_date - date.today()).days
            elif self.is_expired:
                return (self.expiry_date - date.today()).days
        return None
    
    @property
    def trainee_name(self):
        """Get trainee name from enrollment"""
        if self.enrollment and self.enrollment.trainee:
            return self.enrollment.trainee.full_name
        return None
    
    @property
    def trainee_code(self):
        """Get trainee code from enrollment"""
        if self.enrollment and self.enrollment.trainee:
            return self.enrollment.trainee.trainee_code
        return None
    
    @property
    def course_title(self):
        """Get course title from enrollment"""
        if self.enrollment and self.enrollment.batch and self.enrollment.batch.course:
            return self.enrollment.batch.course.course_title
        return None
    
    @property
    def course_code(self):
        """Get course code from enrollment"""
        if self.enrollment and self.enrollment.batch and self.enrollment.batch.course:
            return self.enrollment.batch.course.course_code
        return None
    
    @property
    def batch_name(self):
        """Get batch name from enrollment"""
        if self.enrollment and self.enrollment.batch:
            return self.enrollment.batch.batch_name
        return None
    
    @property
    def grade(self):
        """Get grade from enrollment"""
        if self.enrollment:
            return self.enrollment.grade
        return None
    
    @property
    def approved_by_username(self):
        """Get username of the approver"""
        if self.approved_by_user:
            return self.approved_by_user.username
        return None
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Issued': '✅ Issued',
            'Revoked': '❌ Revoked',
            'Expired': '⏰ Expired',
            'Pending': '⏳ Pending'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def verification_url(self):
        """Get verification URL"""
        if self.verification_token:
            return f"/api/certificates/verify/{self.verification_token}"
        return None
    
    @property
    def is_ready_for_download(self):
        """Check if certificate is ready for download"""
        return self.is_valid and self.certificate_url is not None
    
    @property
    def template_name(self):
        """Get template name"""
        if self.template:
            return self.template.setting_name
        return None
    
    @property
    def template_style(self):
        """Get template style"""
        if self.template:
            return self.template.template_style
        return None
    
    @property
    def enrollment_number(self):
        """Get enrollment number"""
        if self.enrollment:
            return self.enrollment.enrollment_number
        return None
    
    @property
    def age_days(self):
        """Get certificate age in days"""
        if self.issue_date:
            return (date.today() - self.issue_date).days
        return None
    
    # =============================================
    # METHODS
    # =============================================
    
    def mark_as_issued(self):
        """Mark certificate as issued"""
        self.status = 'Issued'
        self.issue_date = date.today()
    
    def mark_as_revoked(self, reason=None):
        """Revoke the certificate"""
        self.status = 'Revoked'
        if reason:
            self.notes = f"Revoked: {reason}"
        elif not self.notes:
            self.notes = "Revoked by administrator"
    
    def mark_as_expired(self):
        """Mark certificate as expired"""
        self.status = 'Expired'
    
    def mark_as_pending(self):
        """Mark certificate as pending"""
        self.status = 'Pending'
    
    def set_expiry(self, days):
        """Set expiry date"""
        self.expiry_date = date.today() + timedelta(days=days)
    
    def generate_verification_url(self):
        """Generate verification URL"""
        if self.verification_token:
            return f"/api/certificates/verify/{self.verification_token}"
        return None
    
    @property
    def is_eligible_for_renewal(self):
        """Check if certificate is eligible for renewal"""
        if self.is_expired and self.status != 'Revoked':
            return True
        return False
    
    def get_certificate_data(self):
        """Get complete certificate data for rendering"""
        return {
            'certificate_number': self.certificate_number,
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'batch_name': self.batch_name,
            'grade': self.grade,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'is_valid': self.is_valid,
            'status': self.status,
            'verification_url': self.verification_url
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert certificate to dictionary"""
        return {
            'certificate_id': self.certificate_id,
            'certificate_number': self.certificate_number,
            'enrollment_id': self.enrollment_id,
            'enrollment_number': self.enrollment_number,
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'batch_name': self.batch_name,
            'grade': self.grade,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'days_until_expiry': self.days_until_expiry,
            'age_days': self.age_days,
            'certificate_url': self.certificate_url,
            'verification_token': self.verification_token,
            'verification_url': self.verification_url,
            'verification_qr': self.verification_qr,
            'issue_reason': self.issue_reason,
            'status': self.status,
            'status_display': self.status_display,
            'is_valid': self.is_valid,
            'is_expired': self.is_expired,
            'is_pending': self.is_pending,
            'is_issued': self.is_issued,
            'is_revoked': self.is_revoked,
            'is_ready_for_download': self.is_ready_for_download,
            'is_eligible_for_renewal': self.is_eligible_for_renewal,
            'approved_by': self.approved_by,
            'approved_by_username': self.approved_by_username,
            'signature_image': self.signature_image,
            'template_id': self.template_id,
            'template_name': self.template_name,
            'template_style': self.template_style,
            'notes': self.notes,
            'certificate_data': self.get_certificate_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert certificate to minimal dictionary"""
        return {
            'certificate_id': self.certificate_id,
            'certificate_number': self.certificate_number,
            'trainee_name': self.trainee_name,
            'course_title': self.course_title,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'status': self.status,
            'is_valid': self.is_valid
        }
    
    def to_dict_public(self):
        """Convert certificate to public dictionary (for verification)"""
        return {
            'certificate_number': self.certificate_number,
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'batch_name': self.batch_name,
            'grade': self.grade,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'issue_reason': self.issue_reason,
            'status': self.status,
            'is_valid': self.is_valid,
            'verification_token': self.verification_token
        }
    
    def __repr__(self):
        return f"<Certificate {self.certificate_number} - {self.trainee_name}>"
