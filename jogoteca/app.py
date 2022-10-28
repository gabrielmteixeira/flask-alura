from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Essa linha tem que estar depois da 'app = Flask(__name__), se não as rotas não vão ser acessadas 
# e vai dar erro 404
from views import *

if __name__ == '__main__':
  app.run(debug=True)