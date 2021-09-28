from . import main
from flask import request,jsonify,make_response
from werkzeug.security import generate_password_hash,check_password_hash
from ..models import User,Covid
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

@main.route('/user/<public_id>/post',methods = ['POST'])
def create_post(public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if user:
        data = request.get_json()
        new_post = Covid(country = data['country'],cases = data['cases'],date_created = data['date_created'],user_id = data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'new covid post created!'}) 
    return jsonify({'message' : 'No user found!'})

@main.route('/user/post', methods = ['GET'])
def get_all_posts():
    posts = Covid.query.all()
    output = []
    for post in posts:
        post_data = {}
        post_data['country'] = post.country
        post_data['cases'] = post.cases
        post_data['date_created'] = post.date_created
        # post_data['user_id'] = post.user_id

        output.append(post_data)

    return jsonify({'posts' : output})   

@main.route('/user/<id>/post', methods = ['GET'])
def get_one_userpost(id):
    post = Covid.query.filter_by(id = id).first()
    if not post:
        return jsonify({'message' : 'No post found!'})
    post_data = {}
    post_data['country'] = post.country
    post_data['cases'] = post.cases
    post_data['date_created'] = post.date_created

    return jsonify({'post' : post_data})     
    

@main.route('/user/<user_id>',methods = ['DELETE'])
def delete_post(user_id):
    post = Covid.query.filter_by(user_id = user_id).first()
    if not post:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(post)
    db.session.commit()    
    return jsonify({'message' : 'Post has been deleted'})    


@main.route('/user/<public_id>/post',methods = ['PUT'])
def update_post(public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if user:
        data = request.get_json()
        new_post = Covid(country = data['country'],cases = data['cases'],date_created = data['date_created'],user_id = data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'covid post successfully updated!'}) 
    return jsonify({'message' : 'No user found!'})

     
    
           


               