from .crudmixin import CRUDMixin
from extensions import db
from datetime import datetime
from flask_login import UserMixin
from .medicalrecord import MedicalRecord

class UserHistory(db.Model, CRUDMixin):
    __tablename__ = "user_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="user_history")
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<UserHistory %r>" % self.id
