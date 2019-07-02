from flask_restful import Resource, reqparse
from database import db
from models import User, AuthToken, Organization
from ciphers.cipher_helper import decipher
from functools import wraps
from bs4 import BeautifulSoup
from urllib.request import urlopen

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('cipher')
parser.add_argument('lang')
parser.add_argument('name')
parser.add_argument('Auth-Token', location='headers')

def this_user():
  token = parser.parse_args()['Auth-Token']
  user = User.query.filter_by(id=token.user_id).first()
  return user

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
    return {'result': decipher(args['cipher'], args['lang'])}
  
class OrganizationController(Resource):
  method_decorators = [authenticate]
  def get(self, org_name):
    org = Organization.query.filter_by(name=org_name).first_or_404()
    users_in_org = User.query.filter_by(org_id=org.id).all()
    users_in_org_list = list(map(lambda u: {'username': u.username, 'role': u.role, 'id': u.id}, users_in_org))
    return {'id': org.id, 'name': org.name, 'users': users_in_org_list}
  
  def post(self, org_name):
    args = parser.parse_args()
    org = Organization.query.filter_by(name=org_name).first()
    if org:
      return {'status': 'error', 'message': 'This organization already exists!'}, 401
    new_org = Organization(org_name)
    db.session.add(new_org)
    db.session.commit()
    # Make user the admin of the new organization
    token = AuthToken.query.filter_by(data=args['Auth-Token']).first()
    req_user = User.query.filter_by(id=token.user_id).first()
    new_org_id = Organization.query.filter_by(name=org_name).first().id
    req_user.org_id = new_org_id
    req_user.role = 'admin'
    db.session.commit()
    return {'status': 'success'}, 201
  
  def put(self, org_name):
    args = parser.parse_args()
    org = Organization.query.filter_by(name=org_name).first_or_404()
    token = AuthToken.query.filter_by(data=args['Auth-Token']).first()
    req_user = User.query.filter_by(id=token.user_id).first()
    # Only allow update if the user is an admin of the organization
    if req_user.role == 'admin' and int(req_user.org_id) == int(org.id):
      if args['name']: org.name = args['name']
      db.session.commit()
      return { 'id': org.id, 'name': org.name }
    return {'status': 'error', 'message': 'You do not have permission to modify this organization!'}, 401
  
class OrganizationList(Resource):
  def get(self):
    orgs = Organization.query.all()
    orgs_list = list(map(lambda o: { 'name': o.name, 'id': o.id }, orgs))
    return orgs_list

class NewsController(Resource):
  def get(self, org_name):
    try:
      news_url='https://news.google.com/news/rss/search?q=%s' % org_name
      with urlopen(news_url) as client:
        xml_page = client.read()
      page=BeautifulSoup(xml_page, 'xml')
      news_list=page.findAll('item')
      return list(map(lambda n: {'title': n.title.text, 'link': n.link.text, 'date': n.pubDate.text}, news_list))
    except:
      return {'status': 'error', 'message': 'News not found!'}, 404
