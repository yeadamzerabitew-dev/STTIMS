from .base import db, BaseModel
from datetime import datetime, date
from decimal import Decimal

class Enrollment(BaseModel):
    __tablename__ = 'enrollments'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    enrollment_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id'), nullable=False)
    
    # =============================================
    # ENROLLMENT DETAILS
    # =============================================
    enrollment_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(
        db.Enum('Enrolled', 'Active', 'Completed', 'Dropped', 'Suspended'),
        default='Enrolled'
    )
    
    # =============================================
    # PAYMENT DETAILS
    # =============================================
    payment_status = db.Column(
        db.Enum('Paid', 'Pending', 'Partial', 'Scholarship'),
        default='Pending'
    )
    payment_amount = db.Column(db.DECIMAL(10, 2), nullable=True)
    payment_date = db.Column(db.Date, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    discount_amount = db.Column(db.DECIMAL(10, 2), default=0.00)
    final_amount = db.Column(db.DECIMAL(10, 2), nullable=True)
    
    # =============================================
    # COMPLETION DETAILS
    # =============================================
    completion_date = db.Column(db.Date, nullable=True)
    completion_percentage = db.Column(db.DECIMAL(5, 2), default=0.00)
    attendance_percentage = db.Column(db.DECIMAL(5, 2), default=0.00)
    grade = db.Column(db.String(2), nullable=True)
    performance_summary = db.Column(db.Text, nullable=True)
    
    # =============================================
    # DROP DETAILS
    # =============================================
    drop_date = db.Column(db.Date, nullable=True)
    drop_reason = db.Column(db.Text, nullable=True)
    
    # =============================================
    # NOTES
    # =============================================
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Trainee relationship (M:1)
    trainee = db.relationship(
        'Trainee', 
        back_populates='enrollments'
    )
    
    # 2. Batch relationship (M:1)
    batch = db.relationship(
        'Batch', 
        back_populates='enrollments'
    )
    
    # 3. Certificate relationship (1:1)
    certificate = db.relationship(
        'Certificate', 
        back_populates='enrollment', 
        uselist=False
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
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
    def is_paid(self):
        """Check if enrollment is paid"""
        return self.payment_status in ['Paid', 'Scholarship']
    
    @property
    def is_partially_paid(self):
        """Check if enrollment is partially paid"""
        return self.payment_status == 'Partial'
    
    @property
    def is_pending(self):
        """Check if payment is pending"""
        return self.payment_status == 'Pending'
    
    @property
    def is_active(self):
        """Check if enrollment is active"""
        return self.status in ['Enrolled', 'Active']
    
    @property
    def is_completed(self):
        """Check if enrollment is completed"""
        return self.status == 'Completed'
    
    @property
    def is_dropped(self):
        """Check if enrollment is dropped"""
        return self.status == 'Dropped'
    
    @property
    def is_suspended(self):
        """Check if enrollment is suspended"""
        return self.status == 'Suspended'
    
    @property
    def is_eligible_for_certificate(self):
        """Check if trainee is eligible for certificate"""
        return (
            self.status == 'Completed' and
            (self.attendance_percentage or 0) >= 75 and
            (self.completion_percentage or 0) >= 80 and
            self.grade is not None and
            self.grade != 'F'
        )
    
    @property
    def has_certificate(self):
        """Check if enrollment has a certificate"""
        return self.certificate is not None
    
    @property
    def amount_due(self):
        """Calculate amount due"""
        if self.final_amount and self.payment_amount is not None:
            return float(self.final_amount) - float(self.payment_amount)
        elif self.final_amount:
            return float(self.final_amount)
        return 0.0
    
    @property
    def payment_received(self):
        """Get total payment received"""
        return float(self.payment_amount) if self.payment_amount else 0.0
    
    @property
    def discount_applied(self):
        """Get discount amount"""
        return float(self.discount_amount) if self.discount_amount else 0.0
    
    @property
    def grade_point(self):
        """Get grade point from grade letter"""
        grade_map = {
            'A+': 4.00, 'A': 4.00, 'A-': 3.75,
            'B+': 3.50, 'B': 3.00, 'B-': 2.75,
            'C+': 2.50, 'C': 2.00, 'C-': 1.75,
            'D': 1.00, 'F': 0.00
        }
        return grade_map.get(self.grade, None)
    
    @property
    def days_since_enrollment(self):
        """Calculate days since enrollment"""
        if self.enrollment_date:
            return (date.today() - self.enrollment_date).days
        return None
    
    @property
    def days_until_completion(self):
        """Calculate days until completion based on batch end date"""
        if self.batch and self.batch.end_date:
            return (self.batch.end_date - date.today()).days
        return None
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Enrolled': '📝 Enrolled',
            'Active': '🔄 Active',
            'Completed': '✅ Completed',
            'Dropped': '❌ Dropped',
            'Suspended': '⏸️ Suspended'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def payment_status_display(self):
        """Get display-friendly payment status"""
        status_map = {
            'Paid': '✅ Paid',
            'Pending': '⏳ Pending',
            'Partial': '💰 Partial',
            'Scholarship': '🎓 Scholarship'
        }
        return status_map.get(self.payment_status, self.payment_status)
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the enrollment"""
        if self.status == 'Enrolled':
            self.status = 'Active'
    
    def complete(self, grade=None):
        """Complete the enrollment"""
        self.status = 'Completed'
        self.completion_date = date.today()
        if grade:
            self.grade = grade
    
    def drop(self, reason=None):
        """Drop the enrollment"""
        self.status = 'Dropped'
        self.drop_date = date.today()
        if reason:
            self.drop_reason = reason
        # Update batch enrollment count
        if self.batch and (self.batch.current_enrollment or 0) > 0:
            self.batch.current_enrollment = (self.batch.current_enrollment or 0) - 1
    
    def suspend(self):
        """Suspend the enrollment"""
        self.status = 'Suspended'
    
    def add_payment(self, amount, method=None):
        """Add a payment"""
        if self.payment_amount is None:
            self.payment_amount = Decimal('0.00')
        self.payment_amount += Decimal(str(amount))
        self.payment_date = date.today()
        if method:
            self.payment_method = method
        self._update_payment_status()
    
    def _update_payment_status(self):
        """Update payment status based on amount paid"""
        if self.final_amount is None:
            return
        
        if self.payment_amount is None or self.payment_amount == Decimal('0.00'):
            self.payment_status = 'Pending'
        elif self.payment_amount >= self.final_amount:
            self.payment_status = 'Paid'
        else:
            self.payment_status = 'Partial'
    
    def get_payment_balance(self):
        """Get the remaining balance"""
        if self.final_amount:
            return float(self.final_amount) - self.payment_received
        return 0.0
    
    def update_attendance_percentage(self):
        """Update attendance percentage from attendance records"""
        if not self.batch:
            return
        
        from models import AttendanceRecord
        sessions = self.batch.sessions.filter_by(status='Completed').all()
        if not sessions:
            return
        
        session_ids = [s.session_id for s in sessions]
        records = AttendanceRecord.query.filter(
            AttendanceRecord.trainee_id == self.trainee_id,
            AttendanceRecord.session_id.in_(session_ids)
        ).all()
        
        if records:
            present_count = sum(1 for r in records if r.status in ['Present', 'Late'])
            self.attendance_percentage = round((present_count / len(sessions)) * 100, 2)
    
    def update_completion_percentage(self):
        """Update completion percentage from assessment results"""
        if not self.batch:
            return
        
        from models import Assessment, TraineeResult
        assessments = Assessment.query.filter_by(
            batch_id=self.batch_id,
            status='Completed'
        ).all()
        
        if not assessments:
            return
        
        assessment_ids = [a.assessment_id for a in assessments]
        results = TraineeResult.query.filter(
            TraineeResult.trainee_id == self.trainee_id,
            TraineeResult.assessment_id.in_(assessment_ids)
        ).all()
        
        if results:
            completed = sum(1 for r in results if r.status in ['Pass', 'Fail'])
            self.completion_percentage = round((completed / len(assessments)) * 100, 2)
    
    def get_certificate_data(self):
        """Get data for certificate generation"""
        return {
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'batch_name': self.batch_name,
            'grade': self.grade,
            'attendance_percentage': self.attendance_percentage,
            'completion_percentage': self.completion_percentage,
            'enrollment_id': self.enrollment_id,
            'enrollment_number': self.enrollment_number
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert enrollment to dictionary"""
        return {
            'enrollment_id': self.enrollment_id,
            'enrollment_number': self.enrollment_number,
            'trainee_id': self.trainee_id,
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'batch_id': self.batch_id,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'status': self.status,
            'status_display': self.status_display,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'is_dropped': self.is_dropped,
            'is_suspended': self.is_suspended,
            'payment_status': self.payment_status,
            'payment_status_display': self.payment_status_display,
            'payment_amount': float(self.payment_amount) if self.payment_amount else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'discount_amount': float(self.discount_amount) if self.discount_amount else 0.0,
            'final_amount': float(self.final_amount) if self.final_amount else None,
            'is_paid': self.is_paid,
            'payment_received': self.payment_received,
            'amount_due': self.amount_due,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'completion_percentage': float(self.completion_percentage) if self.completion_percentage else 0.0,
            'attendance_percentage': float(self.attendance_percentage) if self.attendance_percentage else 0.0,
            'grade': self.grade,
            'grade_point': self.grade_point,
            'performance_summary': self.performance_summary,
            'is_eligible_for_certificate': self.is_eligible_for_certificate,
            'has_certificate': self.has_certificate,
            'drop_date': self.drop_date.isoformat() if self.drop_date else None,
            'drop_reason': self.drop_reason,
            'days_since_enrollment': self.days_since_enrollment,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert enrollment to minimal dictionary"""
        return {
            'enrollment_id': self.enrollment_id,
            'enrollment_number': self.enrollment_number,
            'trainee_name': self.trainee_name,
            'course_title': self.course_title,
            'status': self.status,
            'payment_status': self.payment_status,
            'attendance_percentage': float(self.attendance_percentage) if self.attendance_percentage else 0.0,
            'grade': self.grade
        }
    
    def __repr__(self):
        return f"<Enrollment {self.enrollment_number} - {self.trainee_name}>"
