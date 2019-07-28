from flask_restful import Resource, reqparse
from uuid import uuid4
from hashlib import sha256
from database import db
from models import User, Organization
from controllers.mainControllers import authenticate, generate_token, this_user

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Authorization', location='headers')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('email')
parser.add_argument('role')
parser.add_argument('org_id')

class LoginController(Resource):
  def post(self):
    """The POST handler for the /login endpoint
    
    Returns:
        dict -- Object containing the token and user details
    """
    # Get post arguments
    args = parser.parse_args()
    user = User.query.filter_by(username=args['username']).first()
    # Handle incorrect username or password
    if not user:
      return {'status': 'error', 'message': 'Incorrect username or password.'}, 403
    elif not args['username'] or not args['password']:
        return { 'status': 'error', 'message': 'Invalid user. Please fill in each field!'}, 401
    # Handle login success
    elif user.password == sha256(args['password'].encode()).hexdigest():
      # Create new auth token
      token = generate_token(user)
      # Get user's org
      org = Organization.query.filter_by(id=user.org_id).first();
      return {'token': token, 'user': {'username': user.username, 'id': user.id, 'org_id': user.org_id, 'email': user.email, 'organization': org.name, 'role': user.role}}, 200
    else:
      return {'status': 'error', 'message': 'Invalid username or password.'}

class CreateAccountController(Resource):
  def post(self):
    """The POST handler for the /create_account endpoint
    
    Returns:
        dict -- Status message
    """
    args = parser.parse_args()
    # Check if user exists
    user = User.query.filter_by(username=args['username']).first()
    if user:
      return {'message': 'Username taken!'}, 401
    if not args['username'] or not args['password'] or not args['email']:
      return {'message': 'Please fill in all fields!'}, 401
    # Create user
    new_user = User(args['username'], sha256(args['password'].encode()).hexdigest(), args['email'], args['role'], args['org_id'])
    db.session.add(new_user)
    db.session.commit()
    return {'status': 'success'}, 201
      
class UserList(Resource):
  method_decorators = [authenticate]
  def get(self):
    """The GET hanlder for the /users endpoint
    
    Returns:
        list -- List of users
    """
    users = User.query.all()
    users_list = list(map(lambda u: {'id': u.id, 'username': u.username, 'role': u.role, 'org_id': u.org_id}, users))
    return users_list

class UserController(Resource):
  method_decorators = [authenticate]
  def get(self, user_id):
    """The GET handler for the /users/<user_id> endpoint
    
    Arguments:
        user_id {int} -- The user's id
    
    Returns:
        dict -- Data about the user
    """
    user = User.query.filter_by(id=user_id).first_or_404()
    return {'id': user.id, 'username': user.username, 'role': user.role, 'org_id': user.org_id}
  
  def put(self, user_id):
    """The PUT handler for the /users/<user_id> endpoint
    
    Arguments:
        user_id {int} -- The user's id
    
    Returns:
        dict -- Data about the modified user
    """
    args = parser.parse_args()
    target_user = User.query.filter_by(id=user_id).first_or_404()
    req_user = this_user()
    # Only allow update if the user is modifying self, or the user is an admin modifiying another user in the same org
    if int(req_user['id']) == int(user_id) or req_user['role'] == 'admin' and target_user.org_id == req_user['org_id']:
      if args['username']: target_user.username = args['username']
      if args['org_id']: target_user.org_id = args['org_id']
      if args['email']: target_user.email = args['email']
      if args['password']: target_user.email = args['password']
      if args['role']: target_user.role = args['role']
      db.session.commit()
      org = Organization.query.filter_by(id=target_user.org_id).first()
      return {'id': target_user.id, 'username': target_user.username, 'email': target_user.email, 'role': target_user.role, 'org_id': target_user.org_id, 'organization': org.name}, 200
    return {'message': 'You do not have permission to modify this user!'}, 401
  
  def delete(self, user_id):
    """The DELETE handler for the /users/<user_id> endpoint
    
    Arguments:
        user_id {int} -- The user's id
    
    Returns:
        dict -- Status message
    """
    args = parser.parse_args()
    target_user = User.query.filter_by(id=user_id).first_or_404()
    req_user = this_user()
    # Only allow delete if the user is deleting self, or the user is an admin deleting another user in the same org
    if int(req_user['id']) == int(user_id) or req_user['role'] == 'admin' and int(target_user.org_id) == int(req_user['org_id']):
      db.session.delete(target_user)
      db.session.commit()
      return {'status': 'success'}
    return {'message': 'You do not have permission to delete this user!'}, 401
