from . import main
from flask import request,jsonify,make_response
from werkzeug.security import generate_password_hash,check_password_hash
from ..models import User,Covid,Comment
import uuid
from .. import db
import jwt
import datetime
from functools import wraps

SECRET_KEY  =  'kfgkgkjlkndlclkdslkcndslkvndsvdvuds'

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):#arbitrary functions 
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:    
            return jsonify({'message' : 'Token is missing'}),401

        try:
            data = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            current_user = User.query.filter_by(public_id = data['public_id']).first() 
        except: 
            return jsonify({'message' : 'Token is invalid!'}),401
        return f(current_user,*args, **kwargs)    
    return decorated    


@main.route('/user', methods = ['GET'])
@token_required
def get_all_users(current_user):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['email'] = user.email

        output.append(user_data)

    return jsonify({'users' : output})

@main.route('/user/<public_id>', methods = ['GET'])
@token_required
def get_one_user(current_user,public_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['email'] = user.email


    return jsonify({'user' : user_data})

@main.route('/user', methods = ['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'],method='sha256')

    new_user = User(public_id = str(uuid.uuid4()),name = data['name'],password = hashed_password,email = data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created!'}) 


@main.route('/user/<public_id>',methods = ['DELETE'])
@token_required


def delete_user(current_user,public_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
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
        return jsonify({'message' : 'user not found!'})    
    if check_password_hash(user.password , auth.password): 
        token = jwt.encode({'public_id' : user.public_id, 'exp' :  datetime.datetime.utcnow() + datetime.timedelta(minutes = 180)},SECRET_KEY)

        return jsonify ({'token' : token})
    return jsonify({'message' : 'wrong password or username!'})    



@main.route('/user/<public_id>/post',methods = ['POST'])
@token_required

def create_post(current_user,public_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    user = User.query.filter_by(public_id = public_id).first()
    if user:
        data = request.get_json()
        new_post = Covid(country = data['country'],cases = data['cases'],tests = data['tests'],deaths = data['deaths'],recovered = data['recovered'],date_created = data['date_created'],user_id = data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'new covid post created!'}) 
    return jsonify({'message' : 'No user found!'})

@main.route('/user/post', methods = ['GET'])
@token_required

def get_all_posts(current_user):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    posts = Covid.query.all()
    output = []
    for post in posts:
        post_data = {}
        post_data['country'] = post.country
        post_data['cases'] = post.cases
        post_data['tests'] = post.tests
        post_data['deaths'] = post.deaths
        post_data['recovered'] = post.recovered
        post_data['date_created'] = post.date_created
        post_data['user_id'] = post.user_id

        output.append(post_data)

    return jsonify({'posts' : output})   

@main.route('/user/<user_id>/post', methods = ['GET'])
@token_required

def get_one_user_post(current_user,user_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    
    post = Covid.query.filter_by(user_id = user_id).first()
    if not post:
        return jsonify({'message' : 'No post found!'})
    post_data = {}
    post_data['country'] = post.country
    post_data['cases'] = post.cases
    post_data['tests'] = post.tests
    post_data['deaths'] = post.deaths
    post_data['recovered'] = post.recovered
    post_data['date_created'] = post.date_created
    post_data['user_id'] = post.user_id

    return jsonify({'user_posts' : post_data})     
    

@main.route('/user/post/<user_id>',methods = ['DELETE'])
@token_required

def delete_post(current_user,user_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    post = Covid.query.filter_by(user_id = user_id).first()
    if not post:
        return jsonify({'message' : 'No post found!'})
    db.session.delete(post)
    db.session.commit()    
    return jsonify({'message' : 'Post has been deleted'})    


@main.route('/user/<public_id>/post',methods = ['PUT'])
@token_required

def update_post(current_user,public_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    user = User.query.filter_by(public_id = public_id).first()
    if user:
        data = request.get_json()
        new_post = Covid(country = data['country'],cases = data['cases'],date_created = data['date_created'],user_id = data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'covid post successfully updated!'}) 
    return jsonify({'message' : 'No user found!'})

@main.route('/user/<public_id>/post/comment',methods = ['POST'])
@token_required

def create_comment(current_user,public_id):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    user = User.query.filter_by(public_id = public_id).first()
    if user:
        data = request.get_json()
        new_comment = Comment(text = data['text'],date_created = data['date_created'],author = data['author'])
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'new comment posted'}) 
    return jsonify({'message' : 'No user found!'})

@main.route('/user/post/comment', methods = ['GET'])
@token_required

def get_all_comments(current_user):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    comments = Comment.query.all()
    output = []
    for comment in comments:
        comment_data = {}
        comment_data['text'] = comment.text
        comment_data['date_created'] = comment.date_created
        comment_data['author'] = comment.author

        output.append(comment_data)

    return jsonify({'comments' : output})   


@main.route('/user/post/comment/<author>', methods = ['GET'])
@token_required

def get_single_comment(current_user,author):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    comment = Comment.query.filter_by(author=author).first()
    if not comment:
        return jsonify({'message' : 'No post found!'})    
    comment_data = {}
    comment_data['text'] = comment.text
    comment_data['date_created'] = comment.date_created

    return jsonify({'user_comment' : comment_data})     

@main.route('/user/post/comment/<author>',methods = ['DELETE'])
@token_required

def delete_comment(current_user,author):
    if not current_user:
        return jsonify ({'message' : 'cannot perfom that function!'})
    comment = Comment.query.filter_by(author = author).first()
    if not comment:
        return jsonify({'message' : 'No comment found!'})
    db.session.delete(comment)
    db.session.commit()    
    return jsonify({'message' : 'Comment has been deleted'})    