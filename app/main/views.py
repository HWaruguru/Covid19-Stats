from . import main
from flask import request,jsonify,make_response
from werkzeug.security import generate_password_hash,check_password_hash
from ..models import User
import uuid
from .. import db


@main.route('/user', methods = ['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users' : output})

@main.route('/user/<public_id>', methods = ['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password

    return jsonify({'user' : user_data})

@main.route('/user', methods = ['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'],method='sha256')

    new_user = User(public_id = str(uuid.uuid4()),name = data['name'],password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created!'}) 

@main.route('/user/<public_id>',methods = ['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(user)
    db.session.commit()    
    return jsonify({'message' : 'User has been deleted'})    

@main.route('/login')     
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401,{'WWW-Authenticate' : 'Basic realm = "Login required!"'})

    user = User.query.filter_by(name = auth.username).first()  

    if not user:
        return jsonify({'message' : 'could not verify please recheck username or password'})    
    if check_password_hash(user.password , auth.password): 
        return jsonify ({'message' : 'Login successful!'})
    return jsonify({'message' : 'wrong username or password!'})    

    
    
           


               