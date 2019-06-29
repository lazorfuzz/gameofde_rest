from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from controllers import helloController, userController, mainControllers
from database import db
from models import User, AuthToken

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/gameofde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
# db.drop_all(app=app)
db.create_all(app=app)
api = Api(app)



if __name__ == '__main__':
    api.add_resource(helloController.HelloController, '/hello')
    api.add_resource(userController.LoginController, '/login')
    api.add_resource(userController.CreateAccountController, '/create_account')
    api.add_resource(mainControllers.CaesarController, '/caesar')
    
    app.run(debug=True)
