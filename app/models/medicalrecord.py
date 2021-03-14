from .crudmixin import CRUDMixin
from extensions import db
from datetime import datetime
from flask_login import UserMixin


class MedicalRecord(db.Model, CRUDMixin):
    __tablename__ = "medical_record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="medical_records")

    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
