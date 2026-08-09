from .base import db, BaseModel

class EmergencyContact(BaseModel):
    __tablename__ = 'emergency_contacts'
    
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable=False)
    guardian_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    alternative_phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    
    # =============================================
    # RELATIONSHIP - Using back_populates only
    # =============================================
    trainee = db.relationship('Trainee', back_populates='emergency_contacts')
    
    # =============================================
    # PROPERTIES
    # =============================================
    
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
    def is_primary_contact(self):
        return self.is_primary
    
    # =============================================
    # DICTIONARY CONVERSIONS
    # =============================================
    
    def to_dict(self):
        return {
            'contact_id': self.contact_id,
            'trainee_id': self.trainee_id,
            'trainee_name': self.trainee_name,
            'guardian_name': self.guardian_name,
            'relationship': self.relationship,
            'phone': self.phone,
            'alternative_phone': self.alternative_phone,
            'email': self.email,
            'address': self.address,
            'is_primary': self.is_primary,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<EmergencyContact {self.contact_id} - {self.guardian_name}>"
