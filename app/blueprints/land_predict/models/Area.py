from sqlalchemy import Column, Integer, String, Float, ForeignKey, ForeignKeyConstraint
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
    id_d = db.Column(db.Integer, ForeignKey('dataset.id_d'))
    
    manualdata = relationship('ManualData', backref=backref('areas', uselist=True))
    # dataset = relationship('Dataset', backref=backref('areas', uselist=True))
    dataset = relationship('Dataset', backref=backref('areas', uselist=True))
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['id'], ['manualdata.id_m'],
            name='fk_area_manualdata'
        ),
        db.ForeignKeyConstraint(
            ['id_d'], ['dataset.id_d'],
            name='fk_area_dataset'
        )
    )
    
