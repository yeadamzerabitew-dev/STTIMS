from .base import db, BaseModel
from datetime import datetime

class Notification(BaseModel):
    __tablename__ = 'notifications'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # FOREIGN KEY
    # =============================================
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # =============================================
    # NOTIFICATION DETAILS
    # =============================================
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum('Info', 'Success', 'Warning', 'Error'), default='Info')
    
    # =============================================
    # READ STATUS
    # =============================================
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # =============================================
    # RELATED URL
    # =============================================
    related_url = db.Column(db.String(255), nullable=True)
    
    # =============================================
    # TIMESTAMP
    # =============================================
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # User relationship (M:1) - Many notifications belong to one user
    # Using back_populates to match the relationship in User model
    user = db.relationship(
        'User', 
        back_populates='notifications'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def username(self):
        """Get the username of the notification recipient"""
        if self.user:
            return self.user.username
        return None
    
    @property
    def user_email(self):
        """Get the email of the notification recipient"""
        if self.user:
            return self.user.email
        return None
    
    @property
    def is_info(self):
        return self.type == 'Info'
    
    @property
    def is_success(self):
        return self.type == 'Success'
    
    @property
    def is_warning(self):
        return self.type == 'Warning'
    
    @property
    def is_error(self):
        return self.type == 'Error'
    
    @property
    def is_unread(self):
        return not self.is_read
    
    @property
    def display_type(self):
        """Get display-friendly notification type"""
        type_map = {
            'Info': 'ℹ️ Info',
            'Success': '✅ Success',
            'Warning': '⚠️ Warning',
            'Error': '❌ Error'
        }
        return type_map.get(self.type, self.type)
    
    @property
    def type_class(self):
        """Get CSS class for notification type"""
        type_map = {
            'Info': 'info',
            'Success': 'success',
            'Warning': 'warning',
            'Error': 'danger'
        }
        return type_map.get(self.type, 'info')
    
    @property
    def type_icon(self):
        """Get icon for notification type"""
        icons = {
            'Info': 'info-circle',
            'Success': 'check-circle',
            'Warning': 'exclamation-triangle',
            'Error': 'times-circle'
        }
        return icons.get(self.type, 'bell')
    
    @property
    def type_color(self):
        """Get color for notification type"""
        colors = {
            'Info': 'blue',
            'Success': 'green',
            'Warning': 'yellow',
            'Error': 'red'
        }
        return colors.get(self.type, 'gray')
    
    @property
    def formatted_created_at(self):
        """Get formatted created_at timestamp"""
        if self.created_at:
            return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return None
    
    @property
    def time_ago(self):
        """Get human-readable time since creation"""
        if self.created_at:
            now = datetime.now()
            diff = now - self.created_at
            
            if diff.days > 365:
                years = diff.days // 365
                return f"{years} year{'s' if years > 1 else ''} ago"
            elif diff.days > 30:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
            elif diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                return "Just now"
        return None
    
    # =============================================
    # METHODS
    # =============================================
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        self.is_read = False
        self.read_at = None
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'username': self.username,
            'user_email': self.user_email,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'display_type': self.display_type,
            'type_class': self.type_class,
            'type_icon': self.type_icon,
            'type_color': self.type_color,
            'is_read': self.is_read,
            'is_unread': self.is_unread,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'related_url': self.related_url,
            'created_at': self.formatted_created_at,
            'time_ago': self.time_ago,
            'created_at_iso': self.created_at.isoformat() if self.created_at else None
        }
    
    def to_dict_minimal(self):
        """Convert notification to minimal dictionary"""
        return {
            'notification_id': self.notification_id,
            'title': self.title,
            'type': self.type,
            'is_read': self.is_read,
            'time_ago': self.time_ago
        }
    
    def to_dict_public(self):
        """Convert notification to public dictionary"""
        return {
            'notification_id': self.notification_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'display_type': self.display_type,
            'is_read': self.is_read,
            'time_ago': self.time_ago,
            'related_url': self.related_url
        }
    
    def __repr__(self):
        return f"<Notification {self.notification_id} - {self.title[:30]}>"
