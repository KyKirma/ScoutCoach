from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from routes import *
from models import *
from datascience import atualizarDB, corrigirCSVs

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        corrigirCSVs()
        atualizarDB()
    
    app.run(debug=True)

