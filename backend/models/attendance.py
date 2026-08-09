from .base import db, BaseModel
from datetime import datetime

class AttendanceRecord(BaseModel):
    __tablename__ = 'attendance_records'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    session_id = db.Column(db.Integer, db.ForeignKey('class_sessions.session_id'), nullable=False)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # =============================================
    # ATTENDANCE DETAILS
    # =============================================
    status = db.Column(
        db.Enum('Present', 'Absent', 'Late', 'Excused', 'Holiday', 'Not Applicable'), 
        nullable=False
    )
    check_in_time = db.Column(db.Time, nullable=True)
    check_out_time = db.Column(db.Time, nullable=True)
    remarks = db.Column(db.String(255), nullable=True)
    
    # =============================================
    # METADATA
    # =============================================
    recorded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_verified = db.Column(db.Boolean, default=False)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    session = db.relationship(
        'ClassSession', 
        back_populates='attendance_records'
    )
    
    trainee = db.relationship(
        'Trainee', 
        back_populates='attendance_records'
    )
    
    recorder = db.relationship(
        'User', 
        back_populates='recorded_attendance',
        foreign_keys='AttendanceRecord.recorded_by'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def is_present(self):
        return self.status == 'Present'
    
    @property
    def is_absent(self):
        return self.status == 'Absent'
    
    @property
    def is_late(self):
        return self.status == 'Late'
    
    @property
    def is_excused(self):
        return self.status == 'Excused'
    
    @property
    def is_holiday(self):
        return self.status == 'Holiday'
    
    @property
    def is_na(self):
        return self.status == 'Not Applicable'
    
    @property
    def trainee_name(self):
        """Get trainee full name"""
        if self.trainee:
            return self.trainee.full_name
        return None
    
    @property
    def trainee_code(self):
        """Get trainee code"""
        if self.trainee:
            return self.trainee.trainee_code
        return None
    
    @property
    def session_date(self):
        """Get session date"""
        if self.session:
            return self.session.session_date
        return None
    
    @property
    def session_topic(self):
        """Get session topic"""
        if self.session:
            return self.session.topic_covered
        return None
    
    @property
    def session_type(self):
        """Get session type"""
        if self.session:
            return self.session.session_type
        return None
    
    @property
    def batch_name(self):
        """Get batch name"""
        if self.session and self.session.batch:
            return self.session.batch.batch_name
        return None
    
    @property
    def course_title(self):
        """Get course title"""
        if self.session and self.session.batch and self.session.batch.course:
            return self.session.batch.course.course_title
        return None
    
    @property
    def recorder_name(self):
        """Get recorder username"""
        if self.recorder:
            return self.recorder.username
        return None
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Present': '✅ Present',
            'Absent': '❌ Absent',
            'Late': '⏰ Late',
            'Excused': '📋 Excused',
            'Holiday': '🎉 Holiday',
            'Not Applicable': 'N/A'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def status_color(self):
        """Get color for status"""
        color_map = {
            'Present': 'green',
            'Absent': 'red',
            'Late': 'yellow',
            'Excused': 'blue',
            'Holiday': 'purple',
            'Not Applicable': 'gray'
        }
        return color_map.get(self.status, 'gray')
    
    @property
    def formatted_recorded_at(self):
        """Get formatted recorded_at timestamp"""
        if self.recorded_at:
            return self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        return None
    
    @property
    def duration_minutes(self):
        """Get duration in minutes between check-in and check-out"""
        if self.check_in_time and self.check_out_time:
            in_minutes = self.check_in_time.hour * 60 + self.check_in_time.minute
            out_minutes = self.check_out_time.hour * 60 + self.check_out_time.minute
            return out_minutes - in_minutes
        return None
    
    @property
    def duration_hours(self):
        """Get duration in hours between check-in and check-out"""
        if self.duration_minutes:
            return round(self.duration_minutes / 60, 2)
        return None
    
    @property
    def is_verified_display(self):
        """Get display-friendly verification status"""
        return "✅ Verified" if self.is_verified else "⏳ Unverified"
    
    # =============================================
    # METHODS
    # =============================================
    
    def mark_present(self):
        self.status = 'Present'
    
    def mark_absent(self):
        self.status = 'Absent'
    
    def mark_late(self):
        self.status = 'Late'
    
    def mark_excused(self):
        self.status = 'Excused'
    
    def mark_holiday(self):
        self.status = 'Holiday'
    
    def mark_na(self):
        self.status = 'Not Applicable'
    
    def verify(self):
        self.is_verified = True
    
    def unverify(self):
        self.is_verified = False
    
    def set_check_in(self, time_str):
        from datetime import datetime
        if time_str:
            self.check_in_time = datetime.strptime(time_str, '%H:%M:%S').time()
    
    def set_check_out(self, time_str):
        from datetime import datetime
        if time_str:
            self.check_out_time = datetime.strptime(time_str, '%H:%M:%S').time()
    
    def add_remark(self, remark):
        self.remarks = remark
    
    def get_attendance_summary(self):
        return {
            'attendance_id': self.attendance_id,
            'trainee_name': self.trainee_name,
            'status': self.status,
            'status_display': self.status_display,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'session_topic': self.session_topic,
            'is_verified': self.is_verified
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        return {
            'attendance_id': self.attendance_id,
            'session_id': self.session_id,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'session_topic': self.session_topic,
            'session_type': self.session_type,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'trainee_id': self.trainee_id,
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'status': self.status,
            'status_display': self.status_display,
            'status_color': self.status_color,
            'is_present': self.is_present,
            'is_absent': self.is_absent,
            'is_late': self.is_late,
            'is_excused': self.is_excused,
            'is_holiday': self.is_holiday,
            'is_na': self.is_na,
            'check_in_time': self.check_in_time.strftime('%H:%M') if self.check_in_time else None,
            'check_out_time': self.check_out_time.strftime('%H:%M') if self.check_out_time else None,
            'duration_minutes': self.duration_minutes,
            'duration_hours': self.duration_hours,
            'remarks': self.remarks,
            'recorded_by': self.recorded_by,
            'recorder_name': self.recorder_name,
            'recorded_at': self.formatted_recorded_at,
            'is_verified': self.is_verified,
            'is_verified_display': self.is_verified_display,
            'attendance_summary': self.get_attendance_summary(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        return {
            'attendance_id': self.attendance_id,
            'trainee_name': self.trainee_name,
            'status': self.status,
            'session_date': self.session_date.isoformat() if self.session_date else None
        }
    
    def __repr__(self):
        return f"<AttendanceRecord {self.attendance_id} - {self.trainee_name} - {self.status}>"
