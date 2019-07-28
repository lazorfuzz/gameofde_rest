from flask_restful import Resource, reqparse
import hmac
from hashlib import sha256
from base64 import b64decode, b64encode
import json
from secrets import secret
from datetime import datetime
from database import db
from models import User, Organization, Solution, SavedSolution
from ciphers.CaesarDecipher import decrypt
from functools import wraps
from bs4 import BeautifulSoup
from urllib.request import urlopen
import traceback

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('cipher')
parser.add_argument('lang')
parser.add_argument('solution')
parser.add_argument('org_id')
parser.add_argument('user_id')
parser.add_argument('name')
parser.add_argument('Authorization', location='headers')

def generate_token(user):
  """Generates a JWT-like auth token
  
  Arguments:
      user {User} -- A SequelAlchemy user object
  
  Returns:
      str -- The token
  """

  data = {'id': user.id, 'username': user.username, 'role': user.role, 'org_id': user.org_id, 'created': str(datetime.now())}
  # Serialize user data to JSON, then encode to base64
  b64_data = b64encode(json.dumps(data).encode())
  # Generate a signature with SHA256, then encode to base64
  dig = hmac.new(secret.encode(), msg=b64_data, digestmod=sha256).digest()
  signature = b64encode(dig)
  # Return the token in the format: {user_data}.{signature}
  return '%s.%s' % (b64_data.decode(), signature.decode())


def read_token(token):
  """Validates the token payload with the signature, and returns 
  a dict containing the user data in the payload
  
  Arguments:
      token {str} -- The token passed in the HTTP header
  
  Returns:
      dict -- The decoded user data
  """

  try:
    token = token.split('.')
    payload = token[0].encode()
    # Hash the payload and get the signature
    dig = hmac.new(secret.encode(), msg=payload, digestmod=sha256).digest()
    signature = b64encode(dig)
    # If the signature matches the one provided, return the user data
    if signature.decode() == token[1]:
      data = b64decode(payload).decode()
      user_data = json.loads(data)
      return user_data
    return None
  except: return None

def this_user():
  """Gets the current user's info from token
  
  Returns:
      dict -- The user's data
  """
  token = parser.parse_args()['Authorization']
  user = read_token(token)
  return user

def generic_400(message='Could not understand request'):
  return {'message': message}, 400

def authenticate(func):
  """A decorator method that checks that the user's auth token is valid
  
  Arguments:
      func {func} -- The target method
  
  Returns:
      func -- The target method
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not getattr(func, 'authenticated', True):
      return func(*args, **kwargs)
    token = parser.parse_args()['Authorization']
    user = read_token(token)
    if user != None:
      return func(*args, **kwargs)
    return {'message': 'Invalid auth token.'}, 403
  return wrapper

class CaesarController(Resource):
  method_decorators = [authenticate]
  # Handle cipher entry
  def post(self):
    """The POST handler for the /caesar endpoint
    
    Returns:
        dict -- A dict containing the result and the detected language
    """
    args = parser.parse_args()
    try:
      cipher = args['cipher']
      solution = Solution.query.filter_by(cipher=cipher).first()
      if solution:
        return {'result': solution.solution, 'lang': solution.lang, 'cached': True}
      current_user = this_user()
      deciphered, language = decrypt(cipher, args['lang'])
      new_solution = Solution(cipher, language, deciphered, current_user['id'], current_user['org_id'])
      db.session.add(new_solution)
      db.session.commit()
      return {'result': deciphered, 'lang': language}
    except Exception as e:
      traceback.print_exc()
      return generic_400(str(e))
  
class NoAuthCaesarController(Resource):
  def post(self):
    """The POST handler for the /test_caesar endpoint
    
    Arguments:
        Resource {Resource} -- The Flask Resource
    
    Returns:
        dict -- A dict containing the result and detected language
    """
    args = parser.parse_args()
    try:
      cipher = args['cipher']
      deciphered, language = decrypt(cipher, args['lang'])
      return {'result': deciphered, 'lang': language}
    except Exception as e:
      traceback.print_exc()
      return generic_400(str(e))
  
class OrganizationController(Resource):
  method_decorators = [authenticate]
  def get(self, org_name):
    """The GET handler for /orgs/<org_id> endpoint
    
    Arguments:
        org_name {str} -- The organization's name
    
    Returns:
        dict -- Information about the organization and its list of users
    """
    org = Organization.query.filter_by(name=org_name).first_or_404()
    users_in_org = User.query.filter_by(org_id=org.id).all()
    users_in_org_list = list(map(lambda u: {'username': u.username, 'role': u.role, 'id': u.id}, users_in_org))
    return {'id': org.id, 'name': org.name, 'users': users_in_org_list}
  
  def post(self, org_name):
    """The POST handler for the /orgs/<org_name> endpoint
    
    Arguments:
        org_name {str} -- The organization's name
    
    Returns:
        dict -- A status message
    """
    args = parser.parse_args()
    org = Organization.query.filter_by(name=org_name).first()
    if org:
      return {'status': 'error', 'message': 'This organization already exists!'}, 401
    new_org = Organization(org_name)
    db.session.add(new_org)
    db.session.commit()
    # Make user the admin of the new organization
    req_user = this_user()
    new_org_id = Organization.query.filter_by(name=org_name).first().id
    user = User.query.filter_by(id=req_user['id']).first()
    user.org_id = new_org_id
    user.role = 'admin'
    db.session.commit()
    return {'status': 'success'}, 201
  
  def put(self, org_name):
    """The PUT handler for /orgs/<org_name> endpoint
    
    Arguments:
        org_name {str} -- The organization's name
    
    Returns:
        dict -- Information about the edited organization
    """
    args = parser.parse_args()
    org = Organization.query.filter_by(name=org_name).first_or_404()
    req_user = this_user()
    # Only allow update if the user is an admin of the organization
    if req_user['role'] == 'admin' and int(req_user['org_id']) == int(org.id):
      if args['name']: org.name = args['name']
      db.session.commit()
      return { 'id': org.id, 'name': org.name }
    return {'status': 'error', 'message': 'You do not have permission to modify this organization!'}, 401
  
class OrganizationList(Resource):
  def get(self):
    """The GET handler for the /orgs endpoint
    
    Returns:
        list -- List of organizations
    """
    orgs = Organization.query.all()
    orgs_list = list(map(lambda o: { 'name': o.name, 'id': o.id }, orgs))
    return orgs_list

class NewsController(Resource):
  def get(self, org_name):
    """The GET handler for the /news endpoint
    
    Arguments:
        org_name {str} -- The organization's name
    
    Returns:
        list -- List of news items for the organization
    """
    try:
      news_url='https://news.google.com/news/rss/search?q=%s' % org_name
      with urlopen(news_url) as client:
        xml_page = client.read()
      page=BeautifulSoup(xml_page, 'xml')
      news_list=page.findAll('item')
      return list(map(lambda n: {'title': n.title.text, 'link': n.link.text, 'date': n.pubDate.text}, news_list))
    except:
      return {'status': 'error', 'message': 'News not found!'}, 404

class CheckSolutionController(Resource):
  method_decorators = [authenticate]
  def post(self):
    """The POST handler for the /solutions endpoint
    
    Returns:
        dict -- Data about an existing solution
    """
    try:
      args = parser.parse_args()
      cipher = args['cipher']
      solution = Solution.query.filter_by(cipher=cipher).first_or_404()
      return {'id': solution.id, 'cipher': solution.cipher, 'lang': solution.lang, 'solution': solution.solution, user_id: 'solution.user_id', org_id: 'solution.org_id'}
    except Exception as e:
      return generic_400(str(e))

class SavedSolutionsController(Resource):
  method_decorators = [authenticate]
  def get(self):
    """The GET handler for the /saved_solutions endpoint
    
    Returns:
        list -- List of saved solutions for the requesting user
    """
    try:
      current_user = this_user()
      saved_solutions = SavedSolution.query.filter_by(user_id=current_user['id']).all()
      return list(map(lambda s: {'id': s.id, 'cipher': s.cipher, 'lang': s.lang, 'solution': s.solution, 'user_id': s.user_id}, saved_solutions))
    except Exception as e:
      traceback.print_exc()
      return generic_400(str(e))
  
  def post(self):
    """The POST handler for the /saved_solutions endpoint
    
    Returns:
        dict -- Status message
    """
    try:
      args = parser.parse_args()
      # Create new saved solution
      new_saved_solution = SavedSolution(args['cipher'], args['lang'], args['solution'], args['user_id'])
      db.session.add(new_saved_solution)
      db.session.commit()
      return {'status': 'success'}, 201
    except Exception as e:
      return generic_400(str(e))

class SavedSolutionController(Resource):
  method_decorators = [authenticate]
  def get(self, solution_id):
    """The GET handler for the /saved_solutions/<solution_id> endpoint
    
    Arguments:
        solution_id {int} -- The solution's id
    
    Returns:
        dict -- Object containing the solution data
    """
    try:
      current_user = this_user()
      solution = SavedSolution.query.filter_by(id=solution_id).first_or_404()
      if solution.user_id == current_user['id']:
        return {'id': solution.id, 'cipher': solution.cipher, 'solution': solution.solution, 'user_id': solution.user_id}
      return {'message': 'You do not have permission to access this saved solution!'}, 401
    except Exception as e:
      return generic_400(str(e))
  
  def delete(self, solution_id):
    """The DELETE handler for the /saved_solutions/<solution_id> endpoint
    
    Arguments:
        solution_id {int} -- The solution's id
    
    Returns:
        dict -- Status message
    """
    try:
      current_user = this_user()
      solution = SavedSolution.query.filter_by(id=solution_id).first_or_404()
      if solution.user_id == current_user['id']:
        db.session.delete(solution)
        db.session.commit()
      return {'message': 'Solution deleted!'}
    except Exception as e:
      traceback.print_exc()
      return generic_400(str(e))
