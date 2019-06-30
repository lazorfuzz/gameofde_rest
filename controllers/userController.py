from flask_restful import Resource, reqparse
from uuid import uuid4
from hashlib import sha256
from database import db
from models import User, AuthToken

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('email')
parser.add_argument('role')

class LoginController(Resource):
  # Handle login
  def post(self):
    # Get post arguments
    args = parser.parse_args()
    user = User.query.filter_by(username=args['username']).first()
    # Handle incorrect username or password
    if not user:
      return {'status': 'error', 'message': 'Incorrect username or password.'}, 403
    # Handle login success
    elif user.password == sha256(args['password'].encode()).hexdigest():
      # Delete user's old auth tokens
      old_tokens = AuthToken.query.filter_by(user_id=user.id)
      for old_token in old_tokens:
        db.session.delete(old_token)
      token_data = str(uuid4())
      # Create new auth token
      auth_token = AuthToken(user, token_data)
      db.session.add(auth_token)
      db.session.commit()
      return {'token': token_data}, 200, {'Set-Cookie': 'auth_token=%s;' % token_data}
    else:
      return {'status': 'error', 'message': 'Invalid username or password.'}

class CreateAccountController(Resource):
  # Handle create account
  def post(self):
      args = parser.parse_args()
      # Check if user exists
      user = User.query.filter_by(username=args['username']).first()
      if user:
        return {'status': 'error', 'message': 'User already exists!'}, 403
      # Create user
      new_user = User(args['username'], sha256(args['password'].encode()).hexdigest(), args['email'], args['role'])
      db.session.add(new_user)
      db.session.commit()
      return {'status': 'success'}