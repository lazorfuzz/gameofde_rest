from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from controllers import userController, mainControllers
from database import db
from models import Organization, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/gameofde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
db.init_app(app)
db.drop_all(app=app)
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
api.add_resource(mainControllers.SavedSolutionController, '/saved_solutions/<solution_id>')

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
      db.session.add(User('bob', sha256('lazar'.encode()).hexdigest(), 'boblazar@ufosarereal.org', 'standard', 4))
      db.session.add(User('john', sha256('smith'.encode()).hexdigest(), 'johnsmith@psu.edu', 'standard', 4))
      db.session.add(User('cheney', sha256('dick'.encode()).hexdigest(), 'dickcheney@whitehouse.gov', 'admin', 1))
      db.session.add(User('skywalker', sha256('luke'.encode()).hexdigest(), 'luke@skywalker.com', 'admin', 2))
      db.session.add(User('palpatine', sha256('sidious'.encode()).hexdigest(), 'sheev@naboomail.net', 'admin', 3))
      db.session.commit()
    except: pass

populate_db()

if __name__ == '__main__':
    app.run(debug=True)
