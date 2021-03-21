from .crudmixin import CRUDMixin
from extensions import db

class MedicalRecord(db.Model, CRUDMixin):
    __tablename__ = "medical_record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="medical_records")

    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    systolic_bp = db.Column(db.Float, nullable=False)
    diastolic_bp = db.Column(db.Float, nullable=False)
    cholesterol_level = db.Column(db.String(50), nullable=False)
    blood_glucose_level = db.Column(db.String(50), nullable=False)
    smoking = db.Column(db.String(50), nullable=False)
    alcohol = db.Column(db.String(50), nullable=False)
    physical_activity = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return "<MR %r>" % self.id
