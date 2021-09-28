from . import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.String(250))
    user_id = db.Column(db.Integer)    