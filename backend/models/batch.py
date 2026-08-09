from .base import db, BaseModel
from datetime import datetime, date

class Batch(BaseModel):
    __tablename__ = 'batches'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    batch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    batch_code = db.Column(db.String(20), unique=True, nullable=False)
    batch_name = db.Column(db.String(100), nullable=False)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    # instructor_id - REMOVED from direct relationship
    # instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'), nullable=True)
    
    # =============================================
    # DATES
    # =============================================
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # =============================================
    # SCHEDULE
    # =============================================
    schedule_type = db.Column(db.Enum('Weekday', 'Weekend', 'Evening', 'Intensive'), nullable=False)
    schedule_days = db.Column(db.String(100), nullable=True)
    schedule_time = db.Column(db.Time, nullable=True)
    schedule_end_time = db.Column(db.Time, nullable=True)
    
    # =============================================
    # LOCATION
    # =============================================
    room_number = db.Column(db.String(20), nullable=True)
    building = db.Column(db.String(50), nullable=True)
    
    # =============================================
    # CAPACITY
    # =============================================
    max_capacity = db.Column(db.Integer, nullable=False)
    current_enrollment = db.Column(db.Integer, default=0)
    min_trainees_required = db.Column(db.Integer, default=5)
    
    # =============================================
    # STATUS
    # =============================================
    status = db.Column(db.Enum('Upcoming', 'Ongoing', 'Completed', 'Cancelled'), default='Upcoming')
    
    # =============================================
    # NOTES
    # =============================================
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Course relationship (M:1)
    course = db.relationship('Course', back_populates='batches')
    
    # 2. Enrollments relationship (1:M)
    enrollments = db.relationship('Enrollment', back_populates='batch', lazy='dynamic')
    
    # 3. Class Sessions relationship (1:M)
    sessions = db.relationship('ClassSession', back_populates='batch', lazy='dynamic')
    
    # 4. Assessments relationship (1:M)
    assessments = db.relationship('Assessment', back_populates='batch', lazy='dynamic')
    
    # 5. Course Assignments relationship (1:M)
    course_assignments = db.relationship('CourseAssignment', back_populates='batch', lazy='dynamic')
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def course_title(self):
        """Get the course title"""
        if self.course:
            return self.course.course_title
        return None
    
    @property
    def course_code(self):
        """Get the course code"""
        if self.course:
            return self.course.course_code
        return None
    
    @property
    def instructor_name(self):
        """Get the primary instructor name from course assignments"""
        primary_assignment = self.course_assignments.filter_by(
            role='Primary Instructor',
            status='Active'
        ).first()
        if primary_assignment and primary_assignment.instructor:
            return primary_assignment.instructor.full_name
        return None
    
    @property
    def instructor_id(self):
        """Get the primary instructor ID from course assignments"""
        primary_assignment = self.course_assignments.filter_by(
            role='Primary Instructor',
            status='Active'
        ).first()
        if primary_assignment:
            return primary_assignment.instructor_id
        return None
    
    @property
    def is_upcoming(self):
        return self.status == 'Upcoming'
    
    @property
    def is_ongoing(self):
        return self.status == 'Ongoing'
    
    @property
    def is_completed(self):
        return self.status == 'Completed'
    
    @property
    def is_cancelled(self):
        return self.status == 'Cancelled'
    
    @property
    def is_full(self):
        """Check if batch is full"""
        return (self.current_enrollment or 0) >= (self.max_capacity or 0)
    
    @property
    def is_under_enrolled(self):
        """Check if batch is under enrolled"""
        return (self.current_enrollment or 0) < (self.min_trainees_required or 0)
    
    @property
    def available_slots(self):
        """Get available slots"""
        return max(0, (self.max_capacity or 0) - (self.current_enrollment or 0))
    
    @property
    def occupancy_rate(self):
        """Get occupancy rate percentage"""
        if (self.max_capacity or 0) > 0:
            return round(((self.current_enrollment or 0) / self.max_capacity) * 100, 2)
        return 0
    
    @property
    def duration_days(self):
        """Get batch duration in days"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0
    
    @property
    def duration_weeks(self):
        """Get batch duration in weeks"""
        return round(self.duration_days / 7, 1) if self.duration_days > 0 else 0
    
    @property
    def days_until_start(self):
        """Get days until batch starts"""
        if self.start_date:
            today = date.today()
            if self.start_date >= today:
                return (self.start_date - today).days
            return 0
        return 0
    
    @property
    def days_since_start(self):
        """Get days since batch started"""
        if self.start_date:
            today = date.today()
            if self.start_date <= today:
                return (today - self.start_date).days
            return 0
        return 0
    
    @property
    def days_until_end(self):
        """Get days until batch ends"""
        if self.end_date:
            today = date.today()
            if self.end_date >= today:
                return (self.end_date - today).days
            return 0
        return 0
    
    @property
    def is_started(self):
        """Check if batch has started"""
        if self.start_date:
            return date.today() >= self.start_date
        return False
    
    @property
    def is_ended(self):
        """Check if batch has ended"""
        if self.end_date:
            return date.today() > self.end_date
        return False
    
    @property
    def progress_percentage(self):
        """Get batch progress percentage"""
        if self.start_date and self.end_date:
            total_days = (self.end_date - self.start_date).days
            if total_days > 0:
                elapsed = (date.today() - self.start_date).days
                return round((elapsed / total_days) * 100, 2)
        return 0
    
    @property
    def schedule_display(self):
        """Get display-friendly schedule"""
        if self.schedule_days and self.schedule_time:
            time_str = self.schedule_time.strftime('%H:%M')
            end_time_str = self.schedule_end_time.strftime('%H:%M') if self.schedule_end_time else ''
            return f"{self.schedule_days} at {time_str} - {end_time_str}"
        return self.schedule_type
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Upcoming': '📅 Upcoming',
            'Ongoing': '🔄 Ongoing',
            'Completed': '✅ Completed',
            'Cancelled': '❌ Cancelled'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def schedule_type_display(self):
        """Get display-friendly schedule type"""
        type_map = {
            'Weekday': '📆 Weekday',
            'Weekend': '📆 Weekend',
            'Evening': '🌙 Evening',
            'Intensive': '🔥 Intensive'
        }
        return type_map.get(self.schedule_type, self.schedule_type)
    
    # =============================================
    # METHODS
    # =============================================
    
    def update_enrollment_count(self):
        """Update current enrollment count from active enrollments"""
        from models import Enrollment
        self.current_enrollment = self.enrollments.filter(
            Enrollment.status.in_(['Enrolled', 'Active'])
        ).count()
    
    def can_enroll(self):
        """Check if trainees can enroll in this batch"""
        return (
            self.status in ['Upcoming', 'Ongoing'] and
            not self.is_full and
            self.course.status == 'Active'
        )
    
    def has_seats_available(self):
        """Check if there are seats available"""
        return (self.current_enrollment or 0) < (self.max_capacity or 0)
    
    def can_start(self):
        """Check if batch can be started"""
        return (
            self.status == 'Upcoming' and
            date.today() >= self.start_date and
            (self.current_enrollment or 0) >= (self.min_trainees_required or 0)
        )
    
    def can_complete(self):
        """Check if batch can be completed"""
        return (
            self.status == 'Ongoing' and
            date.today() >= self.end_date
        )
    
    def start(self):
        """Start the batch"""
        if self.can_start():
            self.status = 'Ongoing'
            return True
        return False
    
    def complete(self):
        """Complete the batch"""
        if self.can_complete():
            self.status = 'Completed'
            return True
        return False
    
    def cancel(self):
        """Cancel the batch"""
        if self.status != 'Completed':
            self.status = 'Cancelled'
            return True
        return False
    
    def add_enrollment(self):
        """Increment enrollment count"""
        if self.has_seats_available():
            self.current_enrollment += 1
            return True
        return False
    
    def remove_enrollment(self):
        """Decrement enrollment count"""
        if self.current_enrollment > 0:
            self.current_enrollment -= 1
            return True
        return False
    
    def get_enrollment_stats(self):
        """Get enrollment statistics"""
        total = self.enrollments.count()
        active = self.enrollments.filter_by(status='Active').count()
        completed = self.enrollments.filter_by(status='Completed').count()
        dropped = self.enrollments.filter_by(status='Dropped').count()
        
        return {
            'total': total,
            'active': active,
            'completed': completed,
            'dropped': dropped,
            'occupancy_rate': self.occupancy_rate
        }
    
    def get_session_stats(self):
        """Get session statistics"""
        total = self.sessions.count()
        completed = self.sessions.filter_by(status='Completed').count()
        scheduled = self.sessions.filter_by(status='Scheduled').count()
        cancelled = self.sessions.filter_by(status='Cancelled').count()
        
        return {
            'total': total,
            'completed': completed,
            'scheduled': scheduled,
            'cancelled': cancelled,
            'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0
        }
    
    def get_assessment_stats(self):
        """Get assessment statistics"""
        from models import Assessment
        total = self.assessments.count()
        completed = self.assessments.filter_by(status='Completed').count()
        scheduled = self.assessments.filter_by(status='Scheduled').count()
        ongoing = self.assessments.filter_by(status='Ongoing').count()
        cancelled = self.assessments.filter_by(status='Cancelled').count()
        
        total_weightage = db.session.query(db.func.sum(Assessment.weightage_percent)).filter(
            Assessment.batch_id == self.batch_id,
            Assessment.status != 'Cancelled'
        ).scalar() or 0
        
        return {
            'total': total,
            'completed': completed,
            'scheduled': scheduled,
            'ongoing': ongoing,
            'cancelled': cancelled,
            'total_weightage': float(total_weightage)
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert batch to dictionary"""
        return {
            'batch_id': self.batch_id,
            'batch_code': self.batch_code,
            'batch_name': self.batch_name,
            'course_id': self.course_id,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor_name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration_days': self.duration_days,
            'duration_weeks': self.duration_weeks,
            'schedule_type': self.schedule_type,
            'schedule_type_display': self.schedule_type_display,
            'schedule_days': self.schedule_days,
            'schedule_time': self.schedule_time.strftime('%H:%M') if self.schedule_time else None,
            'schedule_end_time': self.schedule_end_time.strftime('%H:%M') if self.schedule_end_time else None,
            'schedule_display': self.schedule_display,
            'room_number': self.room_number,
            'building': self.building,
            'max_capacity': self.max_capacity,
            'current_enrollment': self.current_enrollment,
            'available_slots': self.available_slots,
            'occupancy_rate': self.occupancy_rate,
            'min_trainees_required': self.min_trainees_required,
            'is_full': self.is_full,
            'is_under_enrolled': self.is_under_enrolled,
            'status': self.status,
            'status_display': self.status_display,
            'is_upcoming': self.is_upcoming,
            'is_ongoing': self.is_ongoing,
            'is_completed': self.is_completed,
            'is_cancelled': self.is_cancelled,
            'is_started': self.is_started,
            'is_ended': self.is_ended,
            'progress_percentage': self.progress_percentage,
            'days_until_start': self.days_until_start,
            'days_since_start': self.days_since_start,
            'days_until_end': self.days_until_end,
            'notes': self.notes,
            'enrollment_stats': self.get_enrollment_stats(),
            'session_stats': self.get_session_stats(),
            'assessment_stats': self.get_assessment_stats(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert batch to minimal dictionary"""
        return {
            'batch_id': self.batch_id,
            'batch_code': self.batch_code,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'current_enrollment': self.current_enrollment,
            'max_capacity': self.max_capacity,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<Batch {self.batch_code} - {self.batch_name}>"
