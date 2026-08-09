from datetime import datetime
from .base import db, BaseModel

class Instructor(BaseModel):
    __tablename__ = 'instructors'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    instructor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # IDENTIFICATION
    # =============================================
    instructor_code = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    
    # =============================================
    # PERSONAL INFORMATION
    # =============================================
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    
    # =============================================
    # CONTACT INFORMATION
    # =============================================
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    
    # =============================================
    # PROFESSIONAL INFORMATION
    # =============================================
    qualification = db.Column(db.Text, nullable=False)
    years_of_experience = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text, nullable=True)
    
    # =============================================
    # EMPLOYMENT INFORMATION
    # =============================================
    status = db.Column(db.Enum('Active', 'Inactive', 'On Leave'), default='Active')
    employment_type = db.Column(db.Enum('Full Time', 'Part Time', 'Contract'), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    
    # =============================================
    # METADATA
    # =============================================
    profile_image = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # 1. User relationship (1:1)
    user = db.relationship(
        'User', 
        back_populates='instructor_profile', 
        uselist=False, 
        foreign_keys='User.instructor_id'
    )
    
    # 2. Specializations relationship (1:M)
    specializations = db.relationship(
        'InstructorSpecialization', 
        back_populates='instructor', 
        lazy='dynamic'
    )
    
    # 3. Course Assignments relationship (1:M)
    course_assignments = db.relationship(
        'CourseAssignment', 
        back_populates='instructor', 
        lazy='dynamic'
    )
    
    # 4. Class Sessions relationship (1:M)
    class_sessions = db.relationship(
        'ClassSession', 
        back_populates='instructor', 
        lazy='dynamic'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def full_name(self):
        """Return the full name of the instructor"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = datetime.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    @property
    def is_active(self):
        return self.status == 'Active'
    
    @property
    def is_on_leave(self):
        return self.status == 'On Leave'
    
    @property
    def is_inactive(self):
        return self.status == 'Inactive'
    
    @property
    def is_full_time(self):
        return self.employment_type == 'Full Time'
    
    @property
    def is_part_time(self):
        return self.employment_type == 'Part Time'
    
    @property
    def is_contract(self):
        return self.employment_type == 'Contract'
    
    @property
    def total_assignments(self):
        """Get total number of course assignments"""
        if hasattr(self, 'course_assignments'):
            return self.course_assignments.count()
        return 0
    
    @property
    def active_assignments(self):
        """Get active course assignments count"""
        if hasattr(self, 'course_assignments'):
            return self.course_assignments.filter_by(status='Active').count()
        return 0
    
    @property
    def completed_assignments(self):
        """Get completed course assignments count"""
        if hasattr(self, 'course_assignments'):
            return self.course_assignments.filter_by(status='Completed').count()
        return 0
    
    @property
    def total_specializations(self):
        """Get total number of specializations"""
        if hasattr(self, 'specializations'):
            return self.specializations.count()
        return 0
    
    @property
    def primary_specialization(self):
        """Get the primary specialization"""
        if hasattr(self, 'specializations'):
            primary = self.specializations.filter_by(is_primary_skill=True).first()
            if primary:
                return primary.skill_name
        return None
    
    @property
    def total_teaching_hours(self):
        """Get total teaching hours from all active assignments"""
        if hasattr(self, 'course_assignments'):
            assignments = self.course_assignments.filter_by(status='Active').all()
            return sum(a.teaching_hours or 0 for a in assignments)
        return 0
    
    @property
    def years_at_institution(self):
        """Calculate years since joining"""
        if self.joining_date:
            today = datetime.now().date()
            return today.year - self.joining_date.year - (
                (today.month, today.day) < (self.joining_date.month, self.joining_date.day)
            )
        return None
    
    @property
    def total_class_sessions(self):
        """Get total class sessions taught"""
        if hasattr(self, 'class_sessions'):
            return self.class_sessions.count()
        return 0
    
    @property
    def completed_sessions(self):
        """Get completed class sessions"""
        if hasattr(self, 'class_sessions'):
            return self.class_sessions.filter_by(status='Completed').count()
        return 0
    
    @property
    def scheduled_sessions(self):
        """Get scheduled class sessions"""
        if hasattr(self, 'class_sessions'):
            return self.class_sessions.filter_by(status='Scheduled').count()
        return 0
    
    @property
    def skill_names(self):
        """Get list of all skill names"""
        if hasattr(self, 'specializations'):
            return [s.skill_name for s in self.specializations.all()]
        return []
    
    @property
    def workload_score(self):
        """Calculate workload score based on assignments and hours"""
        active_assignments = self.active_assignments
        total_hours = self.total_teaching_hours
        return round((active_assignments * 10) + (total_hours * 0.5), 2)
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Active': '✅ Active',
            'Inactive': '❌ Inactive',
            'On Leave': '🌴 On Leave'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def employment_type_display(self):
        """Get display-friendly employment type"""
        type_map = {
            'Full Time': '👔 Full Time',
            'Part Time': '⏰ Part Time',
            'Contract': '📄 Contract'
        }
        return type_map.get(self.employment_type, self.employment_type)
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the instructor"""
        self.status = 'Active'
    
    def deactivate(self):
        """Deactivate the instructor"""
        self.status = 'Inactive'
    
    def set_on_leave(self):
        """Set instructor on leave"""
        self.status = 'On Leave'
    
    def add_specialization(self, skill_name, years_of_experience=0, proficiency_level='Advanced', is_primary_skill=False):
        """Add a specialization to the instructor"""
        from models import InstructorSpecialization
        
        # Check if skill already exists
        existing = self.specializations.filter_by(skill_name=skill_name).first()
        if existing:
            return None, "Skill already exists"
        
        # If setting as primary, unset other primary skills
        if is_primary_skill:
            self.specializations.update({'is_primary_skill': False})
        
        specialization = InstructorSpecialization(
            instructor_id=self.instructor_id,
            skill_name=skill_name,
            years_of_experience=years_of_experience,
            proficiency_level=proficiency_level,
            is_primary_skill=is_primary_skill
        )
        
        return specialization, None
    
    def remove_specialization(self, skill_name):
        """Remove a specialization"""
        if hasattr(self, 'specializations'):
            spec = self.specializations.filter_by(skill_name=skill_name).first()
            if spec:
                db.session.delete(spec)
                return True
        return False
    
    def get_specializations_by_level(self, level):
        """Get specializations by proficiency level"""
        if hasattr(self, 'specializations'):
            return self.specializations.filter_by(proficiency_level=level).all()
        return []
    
    def get_primary_skills(self):
        """Get all primary skills"""
        if hasattr(self, 'specializations'):
            return self.specializations.filter_by(is_primary_skill=True).all()
        return []
    
    def get_assignments_by_status(self, status):
        """Get assignments filtered by status"""
        if hasattr(self, 'course_assignments'):
            return self.course_assignments.filter_by(status=status).all()
        return []
    
    def get_active_assignments(self):
        """Get all active assignments"""
        return self.get_assignments_by_status('Active')
    
    def get_completed_assignments(self):
        """Get all completed assignments"""
        return self.get_assignments_by_status('Completed')
    
    def is_teaching_on_date(self, date):
        """Check if instructor is teaching on a specific date"""
        if hasattr(self, 'class_sessions'):
            return self.class_sessions.filter_by(
                session_date=date,
                status='Scheduled'
            ).first() is not None
        return False
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert instructor to dictionary"""
        return {
            'instructor_id': self.instructor_id,
            'instructor_code': self.instructor_code,
            'full_name': self.full_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'city': self.city,
            'qualification': self.qualification,
            'years_of_experience': self.years_of_experience,
            'bio': self.bio,
            'status': self.status,
            'status_display': self.status_display,
            'employment_type': self.employment_type,
            'employment_type_display': self.employment_type_display,
            'joining_date': self.joining_date.isoformat() if self.joining_date else None,
            'years_at_institution': self.years_at_institution,
            'department': self.department,
            'profile_image': self.profile_image,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_assignments': self.total_assignments,
            'active_assignments': self.active_assignments,
            'completed_assignments': self.completed_assignments,
            'total_specializations': self.total_specializations,
            'primary_specialization': self.primary_specialization,
            'skill_names': self.skill_names,
            'total_teaching_hours': self.total_teaching_hours,
            'workload_score': self.workload_score,
            'total_class_sessions': self.total_class_sessions,
            'completed_sessions': self.completed_sessions,
            'scheduled_sessions': self.scheduled_sessions,
            'is_active': self.is_active,
            'is_on_leave': self.is_on_leave,
            'is_inactive': self.is_inactive,
            'is_full_time': self.is_full_time,
            'is_part_time': self.is_part_time,
            'is_contract': self.is_contract
        }
    
    def to_dict_minimal(self):
        """Convert instructor to minimal dictionary"""
        return {
            'instructor_id': self.instructor_id,
            'instructor_code': self.instructor_code,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'department': self.department,
            'status': self.status,
            'employment_type': self.employment_type,
            'years_of_experience': self.years_of_experience
        }
    
    def to_dict_with_specializations(self):
        """Convert instructor with specializations"""
        data = self.to_dict()
        if hasattr(self, 'specializations'):
            data['specializations'] = [
                {
                    'spec_id': s.spec_id,
                    'skill_name': s.skill_name,
                    'years_of_experience': s.years_of_experience,
                    'proficiency_level': s.proficiency_level,
                    'is_primary_skill': s.is_primary_skill,
                    'skill_description': s.skill_description
                }
                for s in self.specializations.all()
            ]
        return data
    
    def __repr__(self):
        return f"<Instructor {self.instructor_code} - {self.full_name}>"
