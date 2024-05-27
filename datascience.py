import pandas as pd
import os
from main import db
from models import Campeonato, Times, Jogo

CSVPath = "./DataBase"
CSVFiles = os.listdir(CSVPath)

def atualizarDB():
    #?Filtrar as regiões pelas div dos mesmos.
    div_to_regiao = {
    'B': 'Belgica',
    'D': 'Alemanha',
    'E': 'Inglaterra',
    'F': 'França',
    'G': 'Grecia',
    'I': 'Italia',
    'N': 'Holanda',
    'P': 'Portugal',
    'SC': 'Escocia',
    'SP': 'Espanha',
    'T': 'Turquia',
    }

    ListaTimes = []
    ListaCamp = []
    ListaJogos = []
    for arquivos_csv in CSVFiles:
        df = pd.read_csv(os.path.join(CSVPath, arquivos_csv))
        df['Regiao'] = df['Div'].str.extract(r'(\D{1,2})\d?')[0].map(div_to_regiao)
        df['Ano'] = df['Date'].str.extract(r'(\d{4})')

        #Tabela Campeonatos
        div = df['Div'].iloc[0]
        regiao = df['Regiao'].iloc[0]
        ano = df['Ano'].iloc[0]
        nome = "{} {} {}".format(div, regiao, ano)
        ListaCamp.append(Campeonato(div = div, ano = ano, regiao = regiao, nome = nome))

        for index, row in df.iterrows():
            #Tabela Times
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            ListaTimes.append(home_team)
            ListaTimes.append(away_team)

            #Tabela Jogos
            div = row['Div']
            regiao = row['Regiao']
            ano = row['Ano']
            nome = "{} {} {}".format(div, regiao, ano)
            ListaJogos.append(Jogo(nome = nome, div = div, ano = ano, hometeam = home_team, awayteam = away_team, regiao = regiao))

    TimesTotal = list(set(ListaTimes))
    CampTotal = list(set(ListaCamp))
    for itens in TimesTotal:
        db.session.add(Times(nome = itens))
    
    db.session.add_all(CampTotal)
    db.session.add_all(ListaJogos)
    db.session.commit()

