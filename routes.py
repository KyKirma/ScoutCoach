from flask import render_template, redirect, url_for
from main import db, app

@app.route('/')
def home():
    return render_template('default.html')