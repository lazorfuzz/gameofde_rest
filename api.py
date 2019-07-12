from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from controllers import userController, mainControllers
from database import db
from models import Organization, User, AuthToken

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/gameofde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
db.init_app(app)
# db.drop_all(app=app)
db.create_all(app=app)
api = Api(app)

api.add_resource(userController.LoginController, '/login')
api.add_resource(userController.CreateAccountController, '/create_account')
api.add_resource(userController.UserList, '/users')
api.add_resource(userController.UserController, '/users/<user_id>')

api.add_resource(mainControllers.OrganizationList, '/orgs')
api.add_resource(mainControllers.OrganizationController, '/orgs/<org_name>')
api.add_resource(mainControllers.NewsController, '/news/<org_name>')

api.add_resource(mainControllers.CaesarController, '/caesar')
api.add_resource(mainControllers.NoAuthCaesarController, '/test_caesar')
api.add_resource(mainControllers.CheckSolutionController, '/solutions')
api.add_resource(mainControllers.SavedSolutionsController, '/saved_solutions')

def populate_db():
  with app.app_context():
    try:
      db.session.add(Organization('CIA'))
      db.session.add(Organization('DEA'))
      db.session.add(Organization('DHS'))
      db.session.add(Organization('FBI'))
      db.session.add(Organization('KFC'))
      db.session.add(Organization('NSA'))
      db.session.add(User('leon', sha256('test'.encode()).hexdigest(), 'leon@email.net', 'admin', 5))
      db.session.add(User('student', sha256('ist440'.encode()).hexdigest(), 'student@psu.edu', 'admin', 4))
      db.session.commit()
    except: pass

populate_db()

if __name__ == '__main__':
    app.run(debug=True)
