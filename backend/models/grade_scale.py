from .base import db, BaseModel

class GradeScale(BaseModel):
    __tablename__ = 'grade_scale'
    
    grade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade_letter = db.Column(db.String(2), unique=True, nullable=False)
    grade_point = db.Column(db.DECIMAL(3, 2), nullable=False)
    min_percentage = db.Column(db.DECIMAL(5, 2), nullable=False)
    max_percentage = db.Column(db.DECIMAL(5, 2), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    is_pass = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
