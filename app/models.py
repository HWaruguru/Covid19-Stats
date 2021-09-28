from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))    
    covid_posts = db.relationship('Covid',backref = 'user',passive_deletes = True)

class Covid(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer,primary_key = True)  
    country = db.Column(db.String(50))
    cases = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone =True),default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),nullable = False)




    
