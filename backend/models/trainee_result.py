from .base import db, BaseModel
from decimal import Decimal

class TraineeResult(BaseModel):
    __tablename__ = 'trainee_results'
    
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.assessment_id'), nullable=False)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    marks_obtained = db.Column(db.DECIMAL(5, 2), nullable=True)
    percentage_score = db.Column(db.DECIMAL(5, 2), nullable=True)
    grade = db.Column(db.String(2), nullable=True)
    status = db.Column(
        db.Enum('Pass', 'Fail', 'Incomplete', 'Not Attempted'),
        default='Not Attempted'
    )
    comments = db.Column(db.Text, nullable=True)
    instructor_feedback = db.Column(db.Text, nullable=True)
    
    recorded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_verified = db.Column(db.Boolean, default=False)
    
    assessment = db.relationship('Assessment', back_populates='results')
    trainee = db.relationship('Trainee', back_populates='trainee_results')
    recorder = db.relationship(
        'User', 
        back_populates='recorded_results',
        foreign_keys='TraineeResult.recorded_by'
    )
    
    @property
    def is_pass(self):
        return self.status == 'Pass'
    
    @property
    def is_fail(self):
        return self.status == 'Fail'
    
    @property
    def is_incomplete(self):
        return self.status == 'Incomplete'
    
    @property
    def is_not_attempted(self):
        return self.status == 'Not Attempted'
    
    @property
    def trainee_name(self):
        if self.trainee:
            return self.trainee.full_name
        return None
    
    @property
    def trainee_code(self):
        if self.trainee:
            return self.trainee.trainee_code
        return None
    
    @property
    def assessment_title(self):
        if self.assessment:
            return self.assessment.title
        return None
    
    @property
    def assessment_type(self):
        if self.assessment:
            return self.assessment.assessment_type
        return None
    
    @property
    def max_marks(self):
        if self.assessment:
            return self.assessment.max_marks
        return 0
    
    @property
    def percentage(self):
        if self.marks_obtained is not None and self.max_marks > 0:
            return round((float(self.marks_obtained) / self.max_marks) * 100, 2)
        return None
    
    @property
    def grade_point(self):
        grade_map = {
            'A+': 4.00, 'A': 4.00, 'A-': 3.75,
            'B+': 3.50, 'B': 3.00, 'B-': 2.75,
            'C+': 2.50, 'C': 2.00, 'C-': 1.75,
            'D': 1.00, 'F': 0.00
        }
        return grade_map.get(self.grade, None)
    
    @property
    def status_display(self):
        status_map = {
            'Pass': '✅ Pass',
            'Fail': '❌ Fail',
            'Incomplete': '⏳ Incomplete',
            'Not Attempted': '⬜ Not Attempted'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def recorder_name(self):
        if self.recorder:
            return self.recorder.username
        return None
    
    @property
    def formatted_recorded_at(self):
        if self.recorded_at:
            return self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        return None
    
    @property
    def marks_display(self):
        if self.marks_obtained is not None:
            return f"{self.marks_obtained} / {self.max_marks}"
        return "N/A"
    
    @property
    def percentage_display(self):
        if self.percentage is not None:
            return f"{self.percentage}%"
        return "N/A"
    
    @property
    def is_verified_display(self):
        """Get display-friendly verification status"""
        return "✅ Verified" if self.is_verified else "⏳ Unverified"
    
    def mark_pass(self):
        self.status = 'Pass'
    
    def mark_fail(self):
        self.status = 'Fail'
    
    def mark_incomplete(self):
        self.status = 'Incomplete'
    
    def mark_not_attempted(self):
        self.status = 'Not Attempted'
    
    def verify(self):
        self.is_verified = True
    
    def unverify(self):
        self.is_verified = False
    
    def calculate_percentage(self):
        if self.marks_obtained is not None and self.max_marks > 0:
            self.percentage_score = round((float(self.marks_obtained) / self.max_marks) * 100, 2)
            return self.percentage_score
        return None
    
    def set_grade(self):
        if self.percentage_score is not None:
            grade_scale = GradeScale.query.filter(
                GradeScale.min_percentage <= self.percentage_score,
                GradeScale.max_percentage >= self.percentage_score
            ).first()
            if grade_scale:
                self.grade = grade_scale.grade_letter
            return self.grade
        return None
    
    def set_pass_fail(self):
        if self.percentage_score is not None and self.assessment:
            passing_percentage = (self.assessment.passing_marks / self.max_marks) * 100
            if self.percentage_score >= passing_percentage:
                self.status = 'Pass'
            else:
                self.status = 'Fail'
        return self.status
    
    def add_feedback(self, feedback):
        self.instructor_feedback = feedback
    
    def add_comment(self, comment):
        self.comments = comment
    
    def get_result_summary(self):
        return {
            'result_id': self.result_id,
            'trainee_name': self.trainee_name,
            'assessment_title': self.assessment_title,
            'marks_obtained': float(self.marks_obtained) if self.marks_obtained is not None else None,
            'max_marks': self.max_marks,
            'percentage': self.percentage,
            'grade': self.grade,
            'status': self.status,
            'is_verified': self.is_verified
        }
    
    def to_dict(self):
        return {
            'result_id': self.result_id,
            'assessment_id': self.assessment_id,
            'assessment_title': self.assessment_title,
            'assessment_type': self.assessment_type,
            'max_marks': self.max_marks,
            'trainee_id': self.trainee_id,
            'trainee_name': self.trainee_name,
            'trainee_code': self.trainee_code,
            'marks_obtained': float(self.marks_obtained) if self.marks_obtained is not None else None,
            'marks_display': self.marks_display,
            'percentage_score': float(self.percentage_score) if self.percentage_score is not None else None,
            'percentage': self.percentage,
            'percentage_display': self.percentage_display,
            'grade': self.grade,
            'grade_point': self.grade_point,
            'status': self.status,
            'status_display': self.status_display,
            'is_pass': self.is_pass,
            'is_fail': self.is_fail,
            'is_incomplete': self.is_incomplete,
            'is_not_attempted': self.is_not_attempted,
            'comments': self.comments,
            'instructor_feedback': self.instructor_feedback,
            'recorded_by': self.recorded_by,
            'recorder_name': self.recorder_name,
            'recorded_at': self.formatted_recorded_at,
            'is_verified': self.is_verified,
            'is_verified_display': self.is_verified_display,
            'result_summary': self.get_result_summary(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        return {
            'result_id': self.result_id,
            'trainee_name': self.trainee_name,
            'assessment_title': self.assessment_title,
            'marks_obtained': float(self.marks_obtained) if self.marks_obtained is not None else None,
            'percentage_score': float(self.percentage_score) if self.percentage_score is not None else None,
            'grade': self.grade,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<TraineeResult {self.result_id} - {self.trainee_name} - {self.status}>"
