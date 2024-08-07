import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
# URL do campeonato
url = 'https://www.flashscore.com.br/futebol/brasil/brasileirao-betano-2023//resultados'

# Enviar requisição GET para a URL
response = requests.get(url)

# Criar objeto BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar todos os jogos do campeonato
jogos = soup.find_all('div', class_='event__match--twoLine')

# Criar lista para armazenar os links dos jogos
links = []

# Loop para encontrar os links dos jogos
for jogo in jogos:
    link = jogo.find('a')['href']
    links.append(link)

# Criar dicionário para armazenar os dados
dados = {
    "HomeTeam" : [], # Home Nome
    "AwayTeam" : [], # Away Nome
    "DateTime" : [], # Data e Hora
    "FTHG" : [], # FullTime Home Gols
    "FTAG" : [], # FullTime Away Gols
    "HGE": [], # Gols Esperados
    "AGE": [], # Gols Esperados
    "HPB": [],  # Posse de Bola
    "APB": [],  # Posse de Bola
    "HTG": [],  # Tentativa de Gol
    "ATG": [],  # Tentativa de Gol
    "HCG": [],  # Chutes no Gol
    "ACG": [],  # Chutes no Gol
    "HCF": [],  # Chutes para Fora
    "ACF": [],  # Chutes para Fora
    "HCB": [],  # Chutes Bloqueados
    "ACB": [],  # Chutes Bloqueados
    "HFC": [],  # Faltas Cobradas
    "AFC": [],  # Faltas Cobradas
    "HES": [],  # Escanteios
    "AES": [],  # Escanteios
    "HIP": [],  # Impedimentos
    "AIP": [],  # Impedimentos
    "HLC": [],  # Laterais Cobrados
    "ALC": [],  # Laterais Cobrados
    "HDG": [],  # Defesas do Goleiro
    "ADG": [],  # Defesas do Goleiro
    "HFT": [],  # Faltas
    "AFT": [],  # Faltas
    "HCV": [],  # Cartões Vermelhos
    "ACV": [],  # Cartões Vermelhos
    "HCA": [],  # Cartões Amarelos
    "ACA": [],  # Cartões Amarelos
    "HPT": [],  # Passes Totais
    "APT": [],  # Passes Totais
    "HPC": [],  # Passes Completos
    "APC": [],  # Passes Completos
    "HATK": [],  # Ataques
    "AATK": [],  # Ataques
    "HATKP": [],  # Ataques Perigosos
    "AATKP": []  # Ataques Perigosos
}

# Loop para coletar os dados de cada jogo
for link in tqdm(links, total=len(links)):
    try:
        # Enviar requisição GET para o link do jogo
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar os principais atributos
        nomes = soup.find_all('a', class_='participant__participantName')
        nomeHome = nomes[0].text
        nomeAway = nomes[1].text
        hora = soup.find('div', class_='duelParticipant__startTime').text

        dados['HomeTeam'].append(nomeHome)
        dados['AwayTeam'].append(nomeAway)
        dados['DateTime'].append(hora)

        # Encontrar os gols
        golsSpan = soup.find('div', class_='detailScore__wrapper')
        golSpan = golsSpan.find_all('span')
        dados['FTHG'].append(golSpan[0].text)
        dados['FTAG'].append(golSpan[2].text)

        # Encontrar as estatísticas
        navJogo = soup.find_all('div', class_='_tabsSecondary_myv7u_47')
        resultadoBotao = navJogo[0].find_all('a')
        resultadoBotao[1].click()  # Simular clique no botão de estatísticas
        time.sleep(1)  # Aguardar 1 segundo para o carregamento das estatísticas
        sections = soup.find_all('div', class_='_row_1nw75_8')

        # Loop para coletar as estatísticas
        for section in sections:
            try:
                section_text = section.find('div', class_='_category_1nw75_15').text
                if section_text in nomes:
                    home_value = section.find('div', class_='_homeValue_1jbkc_9').text
                    away_value = section.find('div', class_='_awayValue_1jbkc_13').text
                    dados[nomes[section_text]['Home']].append(home_value)
                    dados[nomes[section_text]['Away']].append(away_value)
                else:
                    # Se a chave não for encontrada, preencher com '-'
                    dados[section_text].append('-')
                    dados[section_text].append('-')
            except Exception as error:
                # Se houver um erro, preencher com '-'
                dados[section_text].append('-')
                dados[section_text].append('-')
    except Exception as error:
        print(f'Erro na coleta de dados: {error} \n No jogo {nomeHome} x {nomeAway}')

# Criar DataFrame e salvar em arquivo CSV
df = pd.DataFrame(dados)
filename = 'datasetFlashScore2.csv'
df.to_csv(filename, sep=';', index=False)