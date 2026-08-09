from datetime import datetime
from .base import db, BaseModel

class Setting(BaseModel):
    __tablename__ = 'settings'
    
    setting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Institution settings
    institution_name = db.Column(db.String(100), default='Short-Term Training Institution')
    institution_code = db.Column(db.String(20), default='STTI')
    institution_address = db.Column(db.String(200), default='Addis Ababa, Ethiopia')
    institution_phone = db.Column(db.String(20), default='+251-911-234567')
    institution_email = db.Column(db.String(100), default='info@sttims.com')
    
    # Theme settings
    theme = db.Column(db.String(50), default='default')
    certificate_template = db.Column(db.String(50), default='professional')
    
    # Email settings
    smtp_server = db.Column(db.String(100), default='smtp.gmail.com')
    smtp_port = db.Column(db.Integer, default=587)
    email_address = db.Column(db.String(100), default='noreply@sttims.com')
    email_password = db.Column(db.String(255), nullable=True)
    notifications_enabled = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'setting_id': self.setting_id,
            'institution': {
                'name': self.institution_name,
                'code': self.institution_code,
                'address': self.institution_address,
                'phone': self.institution_phone,
                'email': self.institution_email
            },
            'theme': self.theme,
            'certificate_template': self.certificate_template,
            'email': {
                'smtp_server': self.smtp_server,
                'smtp_port': self.smtp_port,
                'address': self.email_address,
                'notifications_enabled': self.notifications_enabled
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        return {
            'setting_id': self.setting_id,
            'institution_name': self.institution_name,
            'institution_code': self.institution_code,
            'theme': self.theme
        }
