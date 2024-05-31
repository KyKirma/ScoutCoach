from flask import render_template, redirect, url_for
from main import app, db
from models import Campeonato, TPC

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
    #O nome vem no formato: 'Div Regiao Ano'
    info = nome.split()
    timesNoCamp = TPC.query.filter_by(CampAno = str(info[2]), Divisao = str(info[0])).all()

    return render_template('times.html',
                           lista = timesNoCamp)
