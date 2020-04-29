"""Models for Adoption Agency"""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False)

    species = db.Column(db.Text, nullable=False)

    photo_url = db.Column(db.Text, nullable=True, default='https://www.pngitem.com/pimgs/m/30-307416_profile-icon-png-image-free-download-searchpng-employee.png')
    
    age = db.Column(db.Integer, nullable=True)

    notes = db.Column(db.Text, nullable=True)

    available = db.Column(db.Boolean, nullable=False, default=True)


    def __repr__(self):
        u = self
        return f"<Pet id={u.id} name={u.name} species={u.species}>"