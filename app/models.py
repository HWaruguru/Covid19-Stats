from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))  
    email = db.Column(db.String(255),unique = True)  
    covid = db.relationship('Covid',backref = 'user',passive_deletes = True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Covid(db.Model):
    __tablename__ = 'covid'
    id = db.Column(db.Integer,primary_key = True)  
    country = db.Column(db.String(50))
    cases = db.Column(db.String(50000))
    tests = db.Column(db.String(50000))
    deaths = db.Column(db.String(50000))
    recovered = db.Column(db.String(50000))
    date_created = db.Column(db.DateTime(timezone =True),default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),nullable = False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime(timezone =True),default = func.now())
    author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),nullable = False)

