from flask import render_template, redirect, url_for
from main import app
from models import Campeonato, TPC, Jogo

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
                           lista = timesNoCamp,
                           nome = nome)

@app.route('/previsoes/<nome>/<time>')
def timeEscolhido(nome, time):
    #O nome vem no formato: 'Div Regiao Ano'
    jogosTime1 = Jogo.query.filter_by(nome = nome, hometeam = time)
    jogosTime2 = Jogo.query.filter_by(nome = nome, awayteam = time)

    info = nome.split()
    timesNoCamp = TPC.query.filter_by(CampAno = str(info[2]), Divisao = str(info[0])).all()

    return render_template('times.html',
                           listaJ1 = jogosTime1,
                           listaJ2 = jogosTime2,
                           lista = timesNoCamp,
                           nome = nome)

@app.route('/theme')
def tema():
    pass