from flask import render_template, redirect, url_for
from main import db, app
from models import Campeonato

@app.route('/')
def home():
    return render_template('default.html')

@app.route('/previsoes')
def foresee():
    listaSelect = Campeonato.query.order_by(Campeonato.nome)
    return render_template('foresee.html',
                           listaSelect = listaSelect)

@app.route('/previsoes/<nome>')
def campEscolhido(nome):
    redirect(url_for('foresee'))