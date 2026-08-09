from .base import db, BaseModel

class SystemLog(BaseModel):
    __tablename__ = 'system_logs'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # FOREIGN KEY
    # =============================================
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # =============================================
    # LOG DETAILS
    # =============================================
    action_type = db.Column(db.String(50), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    
    # =============================================
    # DATA CHANGES (JSON format)
    # =============================================
    old_values = db.Column(db.Text, nullable=True)
    new_values = db.Column(db.Text, nullable=True)
    
    # =============================================
    # REQUEST INFORMATION
    # =============================================
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    
    # =============================================
    # TIMESTAMP & STATUS
    # =============================================
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default='Success')
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # User relationship (M:1) - Many logs belong to one user
    # Using back_populates to match the relationship in User model
    user = db.relationship(
        'User', 
        back_populates='logs'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def username(self):
        """Get the username of the user who performed the action"""
        if self.user:
            return self.user.username
        return None
    
    @property
    def user_email(self):
        """Get the email of the user who performed the action"""
        if self.user:
            return self.user.email
        return None
    
    @property
    def user_role(self):
        """Get the role of the user who performed the action"""
        if self.user:
            return self.user.role
        return None
    
    @property
    def action_display(self):
        """Get a display-friendly action type"""
        action_map = {
            'CREATE': 'Created',
            'UPDATE': 'Updated',
            'DELETE': 'Deleted',
            'VIEW': 'Viewed',
            'LOGIN': 'Logged In',
            'LOGOUT': 'Logged Out',
            'REGISTER': 'Registered',
            'IMPORT': 'Imported',
            'EXPORT': 'Exported',
            'GENERATE': 'Generated',
            'VERIFY': 'Verified'
        }
        return action_map.get(self.action_type.upper(), self.action_type)
    
    @property
    def is_success(self):
        """Check if the action was successful"""
        return self.status.lower() == 'success'
    
    @property
    def is_error(self):
        """Check if the action resulted in an error"""
        return self.status.lower() == 'error'
    
    @property
    def formatted_timestamp(self):
        """Get formatted timestamp"""
        if self.timestamp:
            return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return None
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Success': '✅ Success',
            'Error': '❌ Error',
            'Warning': '⚠️ Warning'
        }
        return status_map.get(self.status, self.status)
    
    # =============================================
    # METHODS
    # =============================================
    
    def mark_success(self):
        """Mark the log as success"""
        self.status = 'Success'
    
    def mark_error(self, error_message=None):
        """Mark the log as error with optional message"""
        self.status = 'Error'
        if error_message:
            self.new_values = error_message
    
    def get_old_values_dict(self):
        """Get old values as dictionary"""
        if self.old_values:
            try:
                import json
                return json.loads(self.old_values)
            except:
                return {'raw': self.old_values}
        return {}
    
    def get_new_values_dict(self):
        """Get new values as dictionary"""
        if self.new_values:
            try:
                import json
                return json.loads(self.new_values)
            except:
                return {'raw': self.new_values}
        return {}
    
    def get_changes(self):
        """Get the changes made"""
        old = self.get_old_values_dict()
        new = self.get_new_values_dict()
        
        if old and new:
            changes = {}
            for key in new:
                if key in old and old[key] != new[key]:
                    changes[key] = {
                        'old': old[key],
                        'new': new[key]
                    }
            return changes
        return None
    
    def has_changes(self):
        """Check if there are any changes recorded"""
        return self.old_values is not None or self.new_values is not None
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert system log to dictionary"""
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'username': self.username,
            'user_email': self.user_email,
            'user_role': self.user_role,
            'action_type': self.action_type,
            'action_display': self.action_display,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'changes': self.get_changes(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'timestamp': self.formatted_timestamp,
            'status': self.status,
            'status_display': self.status_display,
            'is_success': self.is_success,
            'is_error': self.is_error,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert system log to minimal dictionary"""
        return {
            'log_id': self.log_id,
            'action_type': self.action_type,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'username': self.username,
            'timestamp': self.formatted_timestamp,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<SystemLog {self.log_id} - {self.action_type} on {self.table_name}>"
