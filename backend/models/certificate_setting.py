from .base import db, BaseModel

class CertificateSetting(BaseModel):
    __tablename__ = 'certificate_settings'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    setting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    setting_name = db.Column(db.String(100), nullable=False)
    
    # =============================================
    # FOREIGN KEY
    # =============================================
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=True)
    
    # =============================================
    # TEMPLATE STYLE
    # =============================================
    template_style = db.Column(db.String(50), nullable=False)
    certificate_title = db.Column(db.String(100), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    
    # =============================================
    # SIGNATORIES
    # =============================================
    signature_1_name = db.Column(db.String(100), nullable=True)
    signature_1_title = db.Column(db.String(100), nullable=True)
    signature_2_name = db.Column(db.String(100), nullable=True)
    signature_2_title = db.Column(db.String(100), nullable=True)
    signature_3_name = db.Column(db.String(100), nullable=True)
    signature_3_title = db.Column(db.String(100), nullable=True)
    
    # =============================================
    # DESIGN
    # =============================================
    logo_path = db.Column(db.String(255), nullable=True)
    background_image = db.Column(db.String(255), nullable=True)
    border_style = db.Column(db.String(50), default='Classic')
    font_family = db.Column(db.String(50), default='Times New Roman')
    font_size = db.Column(db.String(10), default='12pt')
    
    # =============================================
    # STATUS & DEFAULT
    # =============================================
    status = db.Column(db.Enum('Active', 'Inactive'), default='Active')
    is_default = db.Column(db.Boolean, default=False)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Course relationship (M:1) - Optional
    course = db.relationship(
        'Course', 
        back_populates='certificate_settings'
    )
    
    # 2. Certificates relationship (1:M)
    certificates = db.relationship(
        'Certificate', 
        back_populates='template', 
        lazy='dynamic'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def is_active(self):
        return self.status == 'Active'
    
    @property
    def is_inactive(self):
        return self.status == 'Inactive'
    
    @property
    def is_default_template(self):
        return self.is_default
    
    @property
    def is_global_default(self):
        """Check if this is the global default template (no course association)"""
        return self.is_default and self.course_id is None
    
    @property
    def is_course_default(self):
        """Check if this is the default template for a specific course"""
        return self.is_default and self.course_id is not None
    
    @property
    def course_title(self):
        """Get course title if associated with a course"""
        if self.course:
            return self.course.course_title
        return None
    
    @property
    def course_code(self):
        """Get course code if associated with a course"""
        if self.course:
            return self.course.course_code
        return None
    
    @property
    def certificate_count(self):
        """Get number of certificates using this template"""
        if hasattr(self, 'certificates'):
            return self.certificates.count()
        return 0
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Active': '✅ Active',
            'Inactive': '❌ Inactive'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def template_style_display(self):
        """Get display-friendly template style"""
        style_map = {
            'Professional': '👔 Professional',
            'Modern': '✨ Modern',
            'Classic': '📜 Classic',
            'Executive': '🏛️ Executive'
        }
        return style_map.get(self.template_style, self.template_style)
    
    @property
    def full_name(self):
        """Get full setting name with course info"""
        if self.course:
            return f"{self.setting_name} ({self.course.course_code})"
        return f"{self.setting_name} (Global)"
    
    @property
    def signatories(self):
        """Get list of signatories"""
        signatories = []
        if self.signature_1_name:
            signatories.append({
                'name': self.signature_1_name,
                'title': self.signature_1_title
            })
        if self.signature_2_name:
            signatories.append({
                'name': self.signature_2_name,
                'title': self.signature_2_title
            })
        if self.signature_3_name:
            signatories.append({
                'name': self.signature_3_name,
                'title': self.signature_3_title
            })
        return signatories
    
    @property
    def has_signatories(self):
        """Check if template has any signatories"""
        return len(self.signatories) > 0
    
    @property
    def placeholder_list(self):
        """Get list of available placeholders"""
        return ['{trainee_name}', '{course_title}', '{grade}', '{issue_date}']
    
    @property
    def missing_placeholders(self):
        """Get missing required placeholders"""
        required = ['{trainee_name}', '{course_title}']
        missing = [p for p in required if p not in self.body_text]
        return missing
    
    @property
    def is_valid_template(self):
        """Check if template has all required placeholders"""
        return len(self.missing_placeholders) == 0
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the template"""
        self.status = 'Active'
    
    def deactivate(self):
        """Deactivate the template"""
        self.status = 'Inactive'
    
    def set_as_default(self):
        """Set this template as default for its course or global"""
        # If course specific, unset other defaults for that course
        if self.course_id:
            CertificateSetting.query.filter_by(
                course_id=self.course_id,
                is_default=True
            ).update({'is_default': False})
        else:
            # Global default
            CertificateSetting.query.filter_by(
                course_id=None,
                is_default=True
            ).update({'is_default': False})
        
        self.is_default = True
    
    def unset_default(self):
        """Unset this template as default"""
        self.is_default = False
    
    def render_certificate(self, trainee_name, course_title, grade, issue_date):
        """Render certificate data with placeholders replaced"""
        body = self.body_text
        body = body.replace('{trainee_name}', trainee_name)
        body = body.replace('{course_title}', course_title)
        body = body.replace('{grade}', grade or 'N/A')
        body = body.replace('{issue_date}', issue_date)
        
        return {
            'title': self.certificate_title,
            'body': body,
            'signatories': self.signatories,
            'style': self.template_style,
            'border_style': self.border_style,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'logo_path': self.logo_path,
            'background_image': self.background_image
        }
    
    def get_placeholders(self):
        """Get list of available placeholders for this template"""
        return self.placeholder_list
    
    def validate_body_text(self):
        """Validate that body text contains required placeholders"""
        return self.missing_placeholders
    
    def update_body_text(self, new_body):
        """Update body text and validate"""
        self.body_text = new_body
        return self.is_valid_template
    
    def add_signatory(self, name, title, position=1):
        """Add or update a signatory"""
        if position == 1:
            self.signature_1_name = name
            self.signature_1_title = title
        elif position == 2:
            self.signature_2_name = name
            self.signature_2_title = title
        elif position == 3:
            self.signature_3_name = name
            self.signature_3_title = title
        else:
            return False
        return True
    
    def remove_signatory(self, position):
        """Remove a signatory"""
        if position == 1:
            self.signature_1_name = None
            self.signature_1_title = None
        elif position == 2:
            self.signature_2_name = None
            self.signature_2_title = None
        elif position == 3:
            self.signature_3_name = None
            self.signature_3_title = None
        else:
            return False
        return True
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert certificate setting to dictionary"""
        return {
            'setting_id': self.setting_id,
            'setting_name': self.setting_name,
            'full_name': self.full_name,
            'course_id': self.course_id,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'template_style': self.template_style,
            'template_style_display': self.template_style_display,
            'certificate_title': self.certificate_title,
            'body_text': self.body_text,
            'signatories': self.signatories,
            'has_signatories': self.has_signatories,
            'signature_1_name': self.signature_1_name,
            'signature_1_title': self.signature_1_title,
            'signature_2_name': self.signature_2_name,
            'signature_2_title': self.signature_2_title,
            'signature_3_name': self.signature_3_name,
            'signature_3_title': self.signature_3_title,
            'logo_path': self.logo_path,
            'background_image': self.background_image,
            'border_style': self.border_style,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'status': self.status,
            'status_display': self.status_display,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'is_global_default': self.is_global_default,
            'is_course_default': self.is_course_default,
            'certificate_count': self.certificate_count,
            'placeholders': self.get_placeholders(),
            'missing_placeholders': self.missing_placeholders,
            'is_valid_template': self.is_valid_template,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert certificate setting to minimal dictionary"""
        return {
            'setting_id': self.setting_id,
            'setting_name': self.setting_name,
            'template_style': self.template_style,
            'status': self.status,
            'is_default': self.is_default
        }
    
    def __repr__(self):
        return f"<CertificateSetting {self.setting_name} - {self.template_style}>"
