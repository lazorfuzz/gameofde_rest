from flask_restful import Resource, reqparse
from database import db
from models import User, AuthToken
from cipher_helper import decipher
from functools import wraps

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('cipher')
parser.add_argument('Auth-Token', location='headers')

def authenticate(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not getattr(func, 'authenticated', True):
      return func(*args, **kwargs)
    token = parser.parse_args()['Auth-Token']
    auth_token = AuthToken.query.filter_by(data=token).first()
    if auth_token:
      return func(*args, **kwargs)
    return {'status': 'error', 'message': 'Invalid auth token.'}, 401
  return wrapper

class CaesarController(Resource):
  method_decorators = [authenticate]
  # Handle cipher entry
  def post(self):
    args = parser.parse_args()
    print('CIPHER', args['cipher'])
    return {'result': decipher(args['cipher'])}