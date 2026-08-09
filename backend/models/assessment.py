from .base import db, BaseModel

class Assessment(BaseModel):
    __tablename__ = 'assessments'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    assessment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    assessment_code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    
    # =============================================
    # FOREIGN KEYS
    # =============================================
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # =============================================
    # ASSESSMENT DETAILS
    # =============================================
    description = db.Column(db.Text, nullable=True)
    assessment_type = db.Column(
        db.Enum('Quiz', 'Midterm', 'Final', 'Practical', 'Project', 'Assignment', 'Lab', 'Presentation'), 
        nullable=False
    )
    max_marks = db.Column(db.Integer, nullable=False)
    weightage_percent = db.Column(db.DECIMAL(5, 2), nullable=False)
    passing_marks = db.Column(db.Integer, nullable=True)
    
    # =============================================
    # SCHEDULE
    # =============================================
    assessment_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    total_questions = db.Column(db.Integer, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    
    # =============================================
    # STATUS
    # =============================================
    status = db.Column(
        db.Enum('Scheduled', 'Ongoing', 'Completed', 'Cancelled'), 
        default='Scheduled'
    )
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. Batch relationship (M:1)
    batch = db.relationship(
        'Batch', 
        back_populates='assessments'
    )
    
    # 2. Results relationship (1:M)
    results = db.relationship(
        'TraineeResult', 
        back_populates='assessment', 
        lazy='dynamic'
    )
    
    # 3. Creator relationship (M:1) - User who created the assessment
    creator = db.relationship(
        'User', 
        back_populates='created_assessments',
        foreign_keys='Assessment.created_by'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def is_quiz(self):
        return self.assessment_type == 'Quiz'
    
    @property
    def is_midterm(self):
        return self.assessment_type == 'Midterm'
    
    @property
    def is_final(self):
        return self.assessment_type == 'Final'
    
    @property
    def is_practical(self):
        return self.assessment_type == 'Practical'
    
    @property
    def is_project(self):
        return self.assessment_type == 'Project'
    
    @property
    def is_assignment(self):
        return self.assessment_type == 'Assignment'
    
    @property
    def is_lab(self):
        return self.assessment_type == 'Lab'
    
    @property
    def is_presentation(self):
        return self.assessment_type == 'Presentation'
    
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
    def total_weightage(self):
        """Get total weightage of all assessments in the batch"""
        if self.batch:
            total = db.session.query(db.func.sum(Assessment.weightage_percent)).filter(
                Assessment.batch_id == self.batch_id,
                Assessment.status != 'Cancelled'
            ).scalar() or 0
            return float(total)
        return 0
    
    @property
    def results_count(self):
        """Get number of results recorded"""
        if hasattr(self, 'results'):
            return self.results.count()
        return 0
    
    @property
    def passed_count(self):
        """Get number of passed results"""
        if hasattr(self, 'results'):
            return self.results.filter_by(status='Pass').count()
        return 0
    
    @property
    def failed_count(self):
        """Get number of failed results"""
        if hasattr(self, 'results'):
            return self.results.filter_by(status='Fail').count()
        return 0
    
    @property
    def pass_rate(self):
        """Get pass rate percentage"""
        total = self.results_count
        if total > 0:
            return round((self.passed_count / total) * 100, 2)
        return 0
    
    @property
    def average_marks(self):
        """Get average marks"""
        from models.trainee_result import TraineeResult
        if self.results_count > 0:
            avg = db.session.query(db.func.avg(TraineeResult.marks_obtained)).filter(
                TraineeResult.assessment_id == self.assessment_id
            ).scalar() or 0
            return round(float(avg), 2)
        return 0
    
    @property
    def average_percentage(self):
        """Get average percentage"""
        from models.trainee_result import TraineeResult
        if self.results_count > 0:
            avg = db.session.query(db.func.avg(TraineeResult.percentage_score)).filter(
                TraineeResult.assessment_id == self.assessment_id
            ).scalar() or 0
            return round(float(avg), 2)
        return 0
    
    @property
    def creator_name(self):
        """Get creator username"""
        if self.creator:
            return self.creator.username
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
    def assessment_type_display(self):
        """Get display-friendly assessment type"""
        type_map = {
            'Quiz': '📝 Quiz',
            'Midterm': '📊 Midterm',
            'Final': '📋 Final',
            'Practical': '🔬 Practical',
            'Project': '📁 Project',
            'Assignment': '📄 Assignment',
            'Lab': '🧪 Lab',
            'Presentation': '🎤 Presentation'
        }
        return type_map.get(self.assessment_type, self.assessment_type)
    
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
    
    # =============================================
    # METHODS
    # =============================================
    
    def mark_as_scheduled(self):
        """Mark assessment as scheduled"""
        self.status = 'Scheduled'
    
    def mark_as_ongoing(self):
        """Mark assessment as ongoing"""
        self.status = 'Ongoing'
    
    def mark_as_completed(self):
        """Mark assessment as completed"""
        self.status = 'Completed'
    
    def mark_as_cancelled(self):
        """Mark assessment as cancelled"""
        self.status = 'Cancelled'
    
    def get_results_summary(self):
        """Get results summary"""
        return {
            'total': self.results_count,
            'passed': self.passed_count,
            'failed': self.failed_count,
            'pass_rate': self.pass_rate,
            'average_marks': self.average_marks,
            'average_percentage': self.average_percentage
        }
    
    def get_results_by_grade(self):
        """Get results grouped by grade"""
        from models.trainee_result import TraineeResult
        grade_distribution = {}
        if hasattr(self, 'results'):
            grades = self.results.filter(
                TraineeResult.grade.isnot(None)
            ).group_by(TraineeResult.grade).with_entities(
                TraineeResult.grade,
                db.func.count(TraineeResult.result_id).label('count')
            ).all()
            
            for grade, count in grades:
                grade_distribution[grade] = count
        return grade_distribution
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert assessment to dictionary"""
        return {
            'assessment_id': self.assessment_id,
            'assessment_code': self.assessment_code,
            'title': self.title,
            'description': self.description,
            'assessment_type': self.assessment_type,
            'assessment_type_display': self.assessment_type_display,
            'batch_id': self.batch_id,
            'batch_name': self.batch_name,
            'course_title': self.course_title,
            'max_marks': self.max_marks,
            'weightage_percent': float(self.weightage_percent),
            'passing_marks': self.passing_marks,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'total_questions': self.total_questions,
            'instructions': self.instructions,
            'status': self.status,
            'status_display': self.status_display,
            'is_scheduled': self.is_scheduled,
            'is_ongoing': self.is_ongoing,
            'is_completed': self.is_completed,
            'is_cancelled': self.is_cancelled,
            'created_by': self.created_by,
            'creator_name': self.creator_name,
            'results_summary': self.get_results_summary(),
            'grade_distribution': self.get_results_by_grade(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert assessment to minimal dictionary"""
        return {
            'assessment_id': self.assessment_id,
            'assessment_code': self.assessment_code,
            'title': self.title,
            'assessment_type': self.assessment_type,
            'max_marks': self.max_marks,
            'weightage_percent': float(self.weightage_percent),
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<Assessment {self.assessment_code} - {self.title}>"
