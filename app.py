from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import view

# 'app' é uma variável que armazena a aplicação
# '__name__' faz referência a esse arquivo, informando onde está a instância do flask, 
# independentemente de onde 'app' estesja sendo utilizado
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
db.init_app(app)
app.register_blueprint(view)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
