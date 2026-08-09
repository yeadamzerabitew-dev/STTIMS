from .base import db, BaseModel
from datetime import datetime, date

class ClassSession(BaseModel):
    __tablename__ = 'class_sessions'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    session_code = db.Column(db.String(20), unique=True, nullable=False)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'), nullable=False)
    
    # =============================================
    # DATE AND TIME
    # =============================================
    session_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # =============================================
    # SESSION DETAILS
    # =============================================
    topic_covered = db.Column(db.String(255), nullable=True)
    session_type = db.Column(
        db.Enum('Lecture', 'Lab', 'Workshop', 'Practical', 'Review', 'Exam'),
        default='Lecture'
    )
    room_number = db.Column(db.String(20), nullable=True)
    
    # =============================================
    # STATUS
    # =============================================
    status = db.Column(
        db.Enum('Scheduled', 'Ongoing', 'Completed', 'Cancelled'),
        default='Scheduled'
    )
    
    # =============================================
    # NOTES
    # =============================================
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Batch relationship (M:1)
    batch = db.relationship('Batch', back_populates='sessions')
    
    # 2. Instructor relationship (M:1)
    instructor = db.relationship('Instructor', back_populates='class_sessions')
    
    # 3. Attendance Records relationship (1:M)
    attendance_records = db.relationship('AttendanceRecord', back_populates='session', lazy='dynamic')
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def batch_name(self):
        """Get the batch name"""
        if self.batch:
            return self.batch.batch_name
        return None
    
    @property
    def course_title(self):
        """Get the course title"""
        if self.batch and self.batch.course:
            return self.batch.course.course_title
        return None
    
    @property
    def instructor_name(self):
        """Get the instructor name"""
        if self.instructor:
            return self.instructor.full_name
        return None
    
    @property
    def is_scheduled(self):
        return self.status == 'Scheduled'
    
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
    def is_past(self):
        """Check if session is in the past"""
        if self.session_date:
            return self.session_date < date.today()
        return False
    
    @property
    def is_today(self):
        """Check if session is today"""
        if self.session_date:
            return self.session_date == date.today()
        return False
    
    @property
    def is_future(self):
        """Check if session is in the future"""
        if self.session_date:
            return self.session_date > date.today()
        return False
    
    @property
    def duration_minutes(self):
        """Get session duration in minutes"""
        if self.start_time and self.end_time:
            start_min = self.start_time.hour * 60 + self.start_time.minute
            end_min = self.end_time.hour * 60 + self.end_time.minute
            return end_min - start_min
        return 0
    
    @property
    def duration_hours(self):
        """Get session duration in hours"""
        return round(self.duration_minutes / 60, 2)
    
    @property
    def session_type_display(self):
        """Get display-friendly session type"""
        type_map = {
            'Lecture': '📚 Lecture',
            'Lab': '🔬 Lab',
            'Workshop': '🛠️ Workshop',
            'Practical': '📝 Practical',
            'Review': '📖 Review',
            'Exam': '📊 Exam'
        }
        return type_map.get(self.session_type, self.session_type)
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Scheduled': '📅 Scheduled',
            'Ongoing': '🔄 Ongoing',
            'Completed': '✅ Completed',
            'Cancelled': '❌ Cancelled'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def day_of_week(self):
        """Get day of week"""
        if self.session_date:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            return days[self.session_date.weekday()]
        return None
    
    @property
    def time_range(self):
        """Get formatted time range"""
        if self.start_time and self.end_time:
            start = self.start_time.strftime('%H:%M')
            end = self.end_time.strftime('%H:%M')
            return f"{start} - {end}"
        return None
    
    @property
    def attendance_count(self):
        """Get total attendance records"""
        if hasattr(self, 'attendance_records'):
            return self.attendance_records.count()
        return 0
    
    @property
    def present_count(self):
        """Get number of present trainees"""
        if hasattr(self, 'attendance_records'):
            return self.attendance_records.filter_by(status='Present').count()
        return 0
    
    @property
    def absent_count(self):
        """Get number of absent trainees"""
        if hasattr(self, 'attendance_records'):
            return self.attendance_records.filter_by(status='Absent').count()
        return 0
    
    @property
    def late_count(self):
        """Get number of late trainees"""
        if hasattr(self, 'attendance_records'):
            return self.attendance_records.filter_by(status='Late').count()
        return 0
    
    @property
    def excused_count(self):
        """Get number of excused trainees"""
        if hasattr(self, 'attendance_records'):
            return self.attendance_records.filter_by(status='Excused').count()
        return 0
    
    @property
    def attendance_rate(self):
        """Get attendance rate"""
        total = self.attendance_count
        if total > 0:
            return round((self.present_count / total) * 100, 2)
        return 0
    
    # =============================================
    # METHODS
    # =============================================
    
    def mark_as_scheduled(self):
        self.status = 'Scheduled'
    
    def mark_as_ongoing(self):
        self.status = 'Ongoing'
    
    def mark_as_completed(self):
        self.status = 'Completed'
    
    def mark_as_cancelled(self):
        self.status = 'Cancelled'
    
    def add_topic(self, topic):
        """Add or update topic covered"""
        self.topic_covered = topic
    
    def assign_instructor(self, instructor_id):
        """Assign an instructor to the session"""
        from models import Instructor
        instructor = Instructor.query.get(instructor_id)
        if instructor and instructor.status == 'Active':
            self.instructor_id = instructor_id
            return True
        return False
    
    def get_attendance_summary(self):
        """Get attendance summary"""
        return {
            'total': self.attendance_count,
            'present': self.present_count,
            'absent': self.absent_count,
            'late': self.late_count,
            'excused': self.excused_count,
            'rate': self.attendance_rate
        }
    
    def get_enrolled_trainees(self):
        """Get list of enrolled trainees for this session"""
        if self.batch:
            return self.batch.enrollments.filter_by(status='Active').all()
        return []
    
    def is_trainee_enrolled(self, trainee_id):
        """Check if a trainee is enrolled in this session's batch"""
        if self.batch:
            return self.batch.enrollments.filter_by(
                trainee_id=trainee_id,
                status='Active'
            ).first() is not None
        return False
    
    def get_trainee_attendance(self, trainee_id):
        """Get attendance record for a specific trainee"""
        if hasattr(self, 'attendance_records'):
            return self.attendance_records.filter_by(trainee_id=trainee_id).first()
        return None
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert class session to dictionary"""
        return {
            'session_id': self.session_id,
            'session_code': self.session_code,
            'batch_id': self.batch_id,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor_name,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'time_range': self.time_range,
            'duration_minutes': self.duration_minutes,
            'duration_hours': self.duration_hours,
            'topic_covered': self.topic_covered,
            'session_type': self.session_type,
            'session_type_display': self.session_type_display,
            'room_number': self.room_number,
            'status': self.status,
            'status_display': self.status_display,
            'is_scheduled': self.is_scheduled,
            'is_ongoing': self.is_ongoing,
            'is_completed': self.is_completed,
            'is_cancelled': self.is_cancelled,
            'is_past': self.is_past,
            'is_today': self.is_today,
            'is_future': self.is_future,
            'notes': self.notes,
            'attendance_summary': self.get_attendance_summary(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert class session to minimal dictionary"""
        return {
            'session_id': self.session_id,
            'session_code': self.session_code,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'topic_covered': self.topic_covered,
            'session_type': self.session_type,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<ClassSession {self.session_code} - {self.session_date}>"
