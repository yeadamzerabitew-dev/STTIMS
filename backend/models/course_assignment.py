from .base import db, BaseModel
from datetime import datetime, date

class CourseAssignment(BaseModel):
    __tablename__ = 'course_assignments'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    assignment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # =============================================
    # ASSIGNMENT DETAILS
    # =============================================
    assignment_date = db.Column(db.Date, nullable=False)
    role = db.Column(
        db.Enum('Primary Instructor', 'Assistant Instructor', 'Teaching Assistant', 'Guest Lecturer'),
        default='Primary Instructor'
    )
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Active', 'Completed', 'Cancelled'), default='Active')
    teaching_hours = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Instructor relationship (M:1)
    instructor = db.relationship(
        'Instructor', 
        back_populates='course_assignments'
    )
    
    # 2. Batch relationship (M:1)
    batch = db.relationship(
        'Batch', 
        back_populates='course_assignments'
    )
    
    # 3. Creator relationship (M:1) - User who created the assignment
    creator = db.relationship(
        'User', 
        back_populates='created_assignments',
        foreign_keys='CourseAssignment.created_by'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def is_active(self):
        return self.status == 'Active'
    
    @property
    def is_completed(self):
        return self.status == 'Completed'
    
    @property
    def is_cancelled(self):
        return self.status == 'Cancelled'
    
    @property
    def is_primary(self):
        return self.role == 'Primary Instructor'
    
    @property
    def is_assistant(self):
        return self.role == 'Assistant Instructor'
    
    @property
    def is_ta(self):
        return self.role == 'Teaching Assistant'
    
    @property
    def is_guest(self):
        return self.role == 'Guest Lecturer'
    
    @property
    def instructor_name(self):
        """Get instructor full name"""
        if self.instructor:
            return self.instructor.full_name
        return None
    
    @property
    def instructor_code(self):
        """Get instructor code"""
        if self.instructor:
            return self.instructor.instructor_code
        return None
    
    @property
    def batch_name(self):
        """Get batch name"""
        if self.batch:
            return self.batch.batch_name
        return None
    
    @property
    def course_title(self):
        """Get course title"""
        if self.batch and self.batch.course:
            return self.batch.course.course_title
        return None
    
    @property
    def course_code(self):
        """Get course code"""
        if self.batch and self.batch.course:
            return self.batch.course.course_code
        return None
    
    @property
    def creator_name(self):
        """Get creator username"""
        if self.creator:
            return self.creator.username
        return None
    
    @property
    def duration_days(self):
        """Get assignment duration in days"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0
    
    @property
    def duration_weeks(self):
        """Get assignment duration in weeks"""
        return round(self.duration_days / 7, 1) if self.duration_days > 0 else 0
    
    @property
    def is_ongoing(self):
        """Check if assignment is currently ongoing"""
        if self.start_date and self.end_date and self.is_active:
            today = date.today()
            return self.start_date <= today <= self.end_date
        return False
    
    @property
    def is_upcoming(self):
        """Check if assignment is upcoming"""
        if self.start_date and self.is_active:
            return self.start_date > date.today()
        return False
    
    @property
    def days_remaining(self):
        """Get days remaining in assignment"""
        if self.end_date and self.is_ongoing:
            return (self.end_date - date.today()).days
        return 0
    
    @property
    def role_display(self):
        """Get display-friendly role"""
        role_map = {
            'Primary Instructor': '👨‍🏫 Primary Instructor',
            'Assistant Instructor': '👨‍🏫 Assistant Instructor',
            'Teaching Assistant': '🧑‍🏫 Teaching Assistant',
            'Guest Lecturer': '👨‍💼 Guest Lecturer'
        }
        return role_map.get(self.role, self.role)
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Active': '✅ Active',
            'Completed': '✅ Completed',
            'Cancelled': '❌ Cancelled'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def teaching_hours_display(self):
        """Get display-friendly teaching hours"""
        if self.teaching_hours:
            return f"{self.teaching_hours} hours"
        return "N/A"
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the assignment"""
        self.status = 'Active'
    
    def complete(self):
        """Complete the assignment"""
        self.status = 'Completed'
    
    def cancel(self):
        """Cancel the assignment"""
        self.status = 'Cancelled'
    
    def is_teaching_on_date(self, date_obj):
        """Check if instructor is teaching on a specific date"""
        return self.start_date <= date_obj <= self.end_date
    
    def get_teaching_schedule(self):
        """Get teaching schedule details"""
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'duration_days': self.duration_days,
            'duration_weeks': self.duration_weeks,
            'teaching_hours': self.teaching_hours,
            'days_remaining': self.days_remaining
        }
    
    def get_batch_details(self):
        """Get batch details for this assignment"""
        if self.batch:
            return {
                'batch_id': self.batch.batch_id,
                'batch_name': self.batch.batch_name,
                'course_title': self.batch.course.course_title if self.batch.course else None,
                'start_date': self.batch.start_date,
                'end_date': self.batch.end_date,
                'status': self.batch.status
            }
        return None
    
    def get_instructor_details(self):
        """Get instructor details for this assignment"""
        if self.instructor:
            return {
                'instructor_id': self.instructor.instructor_id,
                'instructor_code': self.instructor.instructor_code,
                'full_name': self.instructor.full_name,
                'email': self.instructor.email,
                'department': self.instructor.department
            }
        return None
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert course assignment to dictionary"""
        return {
            'assignment_id': self.assignment_id,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor_name,
            'instructor_code': self.instructor_code,
            'instructor_details': self.get_instructor_details(),
            'batch_id': self.batch_id,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'batch_details': self.get_batch_details(),
            'assignment_date': self.assignment_date.isoformat() if self.assignment_date else None,
            'role': self.role,
            'role_display': self.role_display,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration_days': self.duration_days,
            'duration_weeks': self.duration_weeks,
            'status': self.status,
            'status_display': self.status_display,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'is_cancelled': self.is_cancelled,
            'is_ongoing': self.is_ongoing,
            'is_upcoming': self.is_upcoming,
            'is_primary': self.is_primary,
            'is_assistant': self.is_assistant,
            'is_ta': self.is_ta,
            'is_guest': self.is_guest,
            'teaching_hours': self.teaching_hours,
            'teaching_hours_display': self.teaching_hours_display,
            'days_remaining': self.days_remaining,
            'notes': self.notes,
            'created_by': self.created_by,
            'creator_name': self.creator_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert course assignment to minimal dictionary"""
        return {
            'assignment_id': self.assignment_id,
            'instructor_name': self.instructor_name,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'role': self.role,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }
    
    def __repr__(self):
        return f"<CourseAssignment {self.assignment_id} - {self.instructor_name} - {self.batch_name}>"
