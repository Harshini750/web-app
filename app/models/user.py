from .crudmixin import CRUDMixin
from extensions import db
from datetime import datetime
from flask_login import UserMixin
from .medicalrecord import MedicalRecord

class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    medical_records = db.relationship("MedicalRecord", back_populates="user")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.id
