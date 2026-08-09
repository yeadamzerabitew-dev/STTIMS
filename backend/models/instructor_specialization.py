from .base import db, BaseModel

class InstructorSpecialization(BaseModel):
    __tablename__ = 'instructor_specializations'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    spec_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # FOREIGN KEY
    # =============================================
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'), nullable=False)
    
    # =============================================
    # SKILL DETAILS
    # =============================================
    skill_name = db.Column(db.String(100), nullable=False)
    years_of_experience = db.Column(db.Integer, default=0)
    proficiency_level = db.Column(
        db.Enum('Beginner', 'Intermediate', 'Advanced', 'Expert'),
        default='Advanced'
    )
    skill_description = db.Column(db.Text, nullable=True)
    is_primary_skill = db.Column(db.Boolean, default=False)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # Instructor relationship (M:1)
    instructor = db.relationship(
        'Instructor', 
        back_populates='specializations'
    )
    
    # =============================================
    # PROPERTIES
    # =============================================
    
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
    def is_primary(self):
        """Check if this is a primary skill"""
        return self.is_primary_skill
    
    @property
    def proficiency_display(self):
        """Get display-friendly proficiency level"""
        level_map = {
            'Beginner': '🌱 Beginner',
            'Intermediate': '📈 Intermediate',
            'Advanced': '🚀 Advanced',
            'Expert': '🏆 Expert'
        }
        return level_map.get(self.proficiency_level, self.proficiency_level)
    
    @property
    def experience_display(self):
        """Get display-friendly experience"""
        if self.years_of_experience == 0:
            return "Less than 1 year"
        elif self.years_of_experience == 1:
            return "1 year"
        else:
            return f"{self.years_of_experience} years"
    
    @property
    def is_beginner(self):
        return self.proficiency_level == 'Beginner'
    
    @property
    def is_intermediate(self):
        return self.proficiency_level == 'Intermediate'
    
    @property
    def is_advanced(self):
        return self.proficiency_level == 'Advanced'
    
    @property
    def is_expert(self):
        return self.proficiency_level == 'Expert'
    
    @property
    def skill_level_score(self):
        """Get numeric score for proficiency level"""
        level_scores = {
            'Beginner': 1,
            'Intermediate': 2,
            'Advanced': 3,
            'Expert': 4
        }
        return level_scores.get(self.proficiency_level, 0)
    
    @property
    def has_description(self):
        """Check if skill has a description"""
        return self.skill_description is not None and self.skill_description.strip() != ''
    
    # =============================================
    # METHODS
    # =============================================
    
    def set_as_primary(self):
        """Set this skill as primary"""
        # Unset other primary skills for this instructor
        if self.instructor_id:
            InstructorSpecialization.query.filter_by(
                instructor_id=self.instructor_id,
                is_primary_skill=True
            ).update({'is_primary_skill': False})
        self.is_primary_skill = True
    
    def unset_primary(self):
        """Unset as primary skill"""
        self.is_primary_skill = False
    
    def update_proficiency(self, new_level):
        """Update proficiency level"""
        valid_levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        if new_level in valid_levels:
            self.proficiency_level = new_level
            return True
        return False
    
    def add_experience(self, years):
        """Add years of experience"""
        if years > 0:
            self.years_of_experience += years
            return True
        return False
    
    def get_skill_summary(self):
        """Get skill summary"""
        return {
            'skill_name': self.skill_name,
            'proficiency_level': self.proficiency_level,
            'proficiency_display': self.proficiency_display,
            'years_of_experience': self.years_of_experience,
            'experience_display': self.experience_display,
            'is_primary': self.is_primary
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert instructor specialization to dictionary"""
        return {
            'spec_id': self.spec_id,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor_name,
            'instructor_code': self.instructor_code,
            'skill_name': self.skill_name,
            'years_of_experience': self.years_of_experience,
            'experience_display': self.experience_display,
            'proficiency_level': self.proficiency_level,
            'proficiency_display': self.proficiency_display,
            'skill_level_score': self.skill_level_score,
            'is_beginner': self.is_beginner,
            'is_intermediate': self.is_intermediate,
            'is_advanced': self.is_advanced,
            'is_expert': self.is_expert,
            'skill_description': self.skill_description,
            'has_description': self.has_description,
            'is_primary_skill': self.is_primary_skill,
            'is_primary': self.is_primary,
            'skill_summary': self.get_skill_summary(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert instructor specialization to minimal dictionary"""
        return {
            'spec_id': self.spec_id,
            'skill_name': self.skill_name,
            'proficiency_level': self.proficiency_level,
            'years_of_experience': self.years_of_experience,
            'is_primary_skill': self.is_primary_skill
        }
    
    def __repr__(self):
        return f"<InstructorSpecialization {self.spec_id} - {self.skill_name} ({self.proficiency_level})>"
