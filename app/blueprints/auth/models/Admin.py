from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    username = db.Column(db.String(64), nullable=False ,index=True, unique=True)
    email = db.Column(db.String(120), nullable=False , unique=True)
    password_hash = db.Column(db.String(250), nullable=False)

    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.jpg')
    # username: Mapped[str] = mapped_column(String(64), nullable=False ,index=True, unique=True)
    # email: Mapped[str] = mapped_column(String(120), nullable=False , unique=True)
    # password_hash: Mapped[str] = mapped_column(String(250), nullable=False)

    # index=True means that the column is indexed, which can make queries on the 