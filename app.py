from flask import Flask
from Models import db

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/// database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True

migrations = Migrate(app,db)
db.init_app(app)
@app.route('/')
def home():
    return "hello world"

if __name__== '__main__':
    app.run (debug=True, port = 5000)