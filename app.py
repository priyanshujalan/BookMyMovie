#Imports_________________________________________________________________________________________________________
from flask import Flask
from flask import redirect
from flask import url_for

import flask_login

from routes import appRoutes

from models import db
from models import users

#Initialization____________________________________________________________________________________________________
app = Flask(__name__, static_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./bmm.sqlite3"
app.secret_key = 'book_my_movie_bmm'

db.init_app(app)
app.app_context().push()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#Create Database_____________________________________________________________________________________________________________
db.create_all()

#Login Manager Handlers________________________________________________________________________________________________________
@login_manager.user_loader
def load_user(username):
    return users.query.get(username)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('appRoutes.login'))

#Routes______________________________________________________________________________________________________________________
app.register_blueprint(appRoutes)

#Driver Code___________________________________________________________________________________________________________________
if __name__ == "__main__":
    # run the flask app
    app.run(host='0.0.0.0', debug=True, port=5000)
