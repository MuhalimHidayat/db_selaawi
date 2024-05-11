from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy.sql import func 
from app import db, app

class Dataset(db.Model):
    __tablename__ = 'dataset'

    id_d = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(250), nullable=False)
    file_hash = db.Column(db.String(250), nullable=False)
    prediction = db.Column(db.String(250), nullable=False, default='0')
    created_at = db.Column(db.String(250), nullable=False, default=func.now())
    updated_at = db.Column(db.String(250), nullable=False, default=func.now())
    id = db.Column(db.Integer, ForeignKey('admin.id'))

    admin = relationship('Admin',  backref=backref('dataset', uselist=True))