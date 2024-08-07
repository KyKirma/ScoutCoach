from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from routes import *
from Cache.FootballdataukDataScience.models import *
from Cache.FootballdataukDataScience.datascience import atualizarDB, corrigirCSVs

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        corrigirCSVs()
        atualizarDB()
    
    app.run(debug=True, host = '0.0.0.0')

