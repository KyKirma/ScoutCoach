from flask import render_template, redirect, url_for
from main import db, app

@app.route('/')
def home():
    db.create_all()
    return render_template('default.html')

@app.route('/previsoes')
def foresee():
    return render_template('foresee.html')