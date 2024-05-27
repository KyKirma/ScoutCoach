from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pip

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from routes import *
from models import *
from datascience import atualizarDB

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        atualizarDB()

    #try:
    #    pip.main(['install', '-r', 'requirements.txt'])
    #except Exception as e:
    #    print(f"Erro ao instalar pacotes: {e}")
    #finally:
    #    app.run(debug = True)
    app.run(debug=True)

