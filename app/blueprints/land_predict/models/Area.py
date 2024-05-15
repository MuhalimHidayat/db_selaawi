from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy.sql import func
from app import db, app

class Area(db.Model):
    __tablename__ = 'area'
    
    id_area = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(250), nullable=False)
    area_longitude = db.Column(db.Float)
    area_latitude = db.Column(db.Float)
    created_at = db.Column(db.String(250), nullable=False, default=func.now())
    updated_at = db.Column(db.String(250), nullable=False, default=func.now())  
    id = db.Column(db.Integer, ForeignKey('manualdata.id_m'))
    
    manualdata = relationship('ManualData', backref=backref('area', uselist=True))