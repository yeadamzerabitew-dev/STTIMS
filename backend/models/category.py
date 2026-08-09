from .base import db, BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    
    # =============================================
    # PRIMARY KEY
    # =============================================
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # =============================================
    # CATEGORY IDENTIFICATION
    # =============================================
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    category_code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    
    # =============================================
    # STATUS
    # =============================================
    status = db.Column(db.Enum('Active', 'Inactive'), default='Active')
    
    # =============================================
    # SELF-REFERENTIAL FOREIGN KEY
    # =============================================
    parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    
    # =============================================
    # RELATIONSHIPS - Using back_populates
    # =============================================
    
    # Self-referential relationship
    # A category can have many subcategories
    subcategories = db.relationship(
        'Category', 
        back_populates='parent_category'
    )
    
    # A category belongs to one parent category
    parent_category = db.relationship(
        'Category', 
        back_populates='subcategories', 
        remote_side=[category_id]
    )
    
    # 2. Courses relationship (1:M)
    courses = db.relationship('Course', back_populates='category', lazy='dynamic')
    
    # =============================================
    # PROPERTIES
    # =============================================
    
    @property
    def is_active(self):
        return self.status == 'Active'
    
    @property
    def is_inactive(self):
        return self.status == 'Inactive'
    
    @property
    def is_root(self):
        """Check if this is a root category (no parent)"""
        return self.parent_category_id is None
    
    @property
    def has_subcategories(self):
        """Check if category has subcategories"""
        if hasattr(self, 'subcategories'):
            return len(self.subcategories) > 0
        return False
    
    @property
    def subcategory_count(self):
        """Get number of subcategories"""
        if hasattr(self, 'subcategories'):
            return len(self.subcategories)
        return 0
    
    @property
    def course_count(self):
        """Get number of courses in this category"""
        if hasattr(self, 'courses'):
            return self.courses.count()
        return 0
    
    @property
    def active_course_count(self):
        """Get number of active courses in this category"""
        if hasattr(self, 'courses'):
            return self.courses.filter_by(status='Active').count()
        return 0
    
    @property
    def parent_name(self):
        """Get parent category name"""
        if self.parent_category:
            return self.parent_category.category_name
        return None
    
    @property
    def full_path(self):
        """Get full category path (parent > child)"""
        if self.parent_category:
            return f"{self.parent_category.category_name} > {self.category_name}"
        return self.category_name
    
    @property
    def level(self):
        """Get category level (0 for root)"""
        level = 0
        current = self
        while current.parent_category:
            level += 1
            current = current.parent_category
        return level
    
    @property
    def status_display(self):
        """Get display-friendly status"""
        status_map = {
            'Active': '✅ Active',
            'Inactive': '❌ Inactive'
        }
        return status_map.get(self.status, self.status)
    
    # =============================================
    # METHODS
    # =============================================
    
    def activate(self):
        """Activate the category"""
        self.status = 'Active'
    
    def deactivate(self):
        """Deactivate the category"""
        self.status = 'Inactive'
    
    def get_all_subcategories(self):
        """Get all subcategories (including nested)"""
        result = []
        if hasattr(self, 'subcategories'):
            for sub in self.subcategories:
                result.append(sub)
                result.extend(sub.get_all_subcategories())
        return result
    
    def get_all_courses(self):
        """Get all courses in this category and subcategories"""
        courses = []
        if hasattr(self, 'courses'):
            courses.extend(self.courses.all())
        if hasattr(self, 'subcategories'):
            for sub in self.subcategories:
                courses.extend(sub.get_all_courses())
        return courses
    
    def get_tree(self):
        """Get category tree as dictionary"""
        return {
            'category': self.to_dict(),
            'subcategories': [
                sub.get_tree() for sub in self.subcategories
            ] if hasattr(self, 'subcategories') else []
        }
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'category_code': self.category_code,
            'description': self.description,
            'icon': self.icon,
            'display_order': self.display_order,
            'status': self.status,
            'status_display': self.status_display,
            'is_active': self.is_active,
            'is_root': self.is_root,
            'parent_category_id': self.parent_category_id,
            'parent_name': self.parent_name,
            'full_path': self.full_path,
            'level': self.level,
            'subcategory_count': self.subcategory_count,
            'has_subcategories': self.has_subcategories,
            'course_count': self.course_count,
            'active_course_count': self.active_course_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Convert category to minimal dictionary"""
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'category_code': self.category_code,
            'status': self.status
        }
    
    def to_dict_with_tree(self):
        """Convert category with full tree"""
        return self.get_tree()
    
    def __repr__(self):
        return f"<Category {self.category_code} - {self.category_name}>"
