from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy.sql import func
from app import db, app

# from app.blueprints.auth.models.Admin import Admin
class ManualData(db.Model):
    __tablename__ = 'manualdata'

    id_m = db.Column(db.Integer, primary_key=True)
    hum = db.Column(db.Float, nullable=False)
    soil_nitro1 = db.Column(db.Float, nullable=False)
    soil_phos1 = db.Column(db.Float, nullable=False)
    soil_pot1 = db.Column(db.Float, nullable=False)
    soil_temp1 = db.Column(db.Float, nullable=False)
    soil_ph1 = db.Column(db.Float, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(250))
    created_at = db.Column(db.String(250), nullable=False, default=func.now())
    updated_at = db.Column(db.String(250), nullable=False, default=func.now())
    id = db.Column(db.Integer, ForeignKey('admin.id'))

    admin = relationship('Admin',  backref=backref('manualdata', uselist=True))