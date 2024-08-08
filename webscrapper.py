# Importando o webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-crash-reporter')
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')
options.add_experimental_option('detach', False)

# Criando o driver "bot"
driver = webdriver.Chrome(options=options)

# Bibliotecas extras
import time
import pandas as pd
import logging
from tqdm import tqdm

logging.basicConfig(filename='webscrapper.log', level='INFO')
""" driver.get("https://www.flashscore.com.br/futebol/brasil/brasileirao-betano-2023//resultados") 
time.sleep(2) """

# Dados coletados
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

nomes = {
    'Gols Esperados (xG)': {
        'Home': 'HGE',
        'Away': 'AGE'
    },
    'Posse de Bola': {
        'Home': 'HPB',
        'Away': 'APB'
    },
    'Tentativas de Gol': {
        'Home': 'HTG',
        'Away': 'ATG'
    },
    'Chutes no Gol': {
        'Home': 'HCG',
        'Away': 'ACG'
    },
    'Chutes para Fora': {
        'Home': 'HCF',
        'Away': 'ACF'
    },
    'Chutes Bloqueados': {
        'Home': 'HCB',
        'Away': 'ACB'
    },
    'Faltas Cobradas': {
        'Home': 'HFC',
        'Away': 'AFC'
    },
    'Escanteios': {
        'Home': 'HES',
        'Away': 'AES'
    },
    'Impedimentos': {
        'Home': 'HIP',
        'Away': 'AIP'
    },
    'Laterais Cobrados': {
        'Home': 'HLC',
        'Away': 'ALC'
    },
    'Defesas do Goleiro': {
        'Home': 'HDG',
        'Away': 'ADG'
    },
    'Faltas': {
        'Home': 'HFT',
        'Away': 'AFT'
    },
    'Cartões Vermelhos': {
        'Home': 'HCV',
        'Away': 'ACV'
    },
    'Cartões Amarelos': {
        'Home': 'HCA',
        'Away': 'ACA'
    },
    'Passes Totais': {
        'Home': 'HPT',
        'Away': 'APT'
    },
    'Passes Completados': {
        'Home': 'HPC',
        'Away': 'APC'
    },
    'Ataques': {
        'Home': 'HATK',
        'Away': 'AATK'
    },
    'Ataques Perigosos': {
        'Home': 'HATKP',
        'Away': 'AATKP'
    }
}
# Algoritmo para cada campeonato
""" eventosCampeonato = driver.find_elements(By.CSS_SELECTOR, 'div.archive__row')
linksCamp = []
for evento in eventosCampeonato:
    link = evento.find_element(By.CSS_SELECTOR, 'a')
    linksCamp.append(f"{link.get_attribute("href")}/resultados")

# Filtro de seleção de campeonato
campSelecionado = linksCamp[1] """

logging.info('Iniciando o programa')
campSelecionado = 'https://www.flashscore.com.br/futebol/brasil/brasileirao-betano-2022//resultados'
logging.info(f'Capturando os dados de [{campSelecionado}]')
print('Programa será iniciado, qualquer evento e erro será gravado em webscrapper.log')

driver.get(campSelecionado)
time.sleep(1)

# Aceitar Cookies
cookieBnt = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
cookieBnt.click()
time.sleep(5)

# Abrir todas as sanfonas
sanfonas = driver.find_element(By.CSS_SELECTOR, 'a.event__more')
if sanfonas:
    try:
        while sanfonas:
            sanfonas.click()
            time.sleep(3)
            sanfonas = driver.find_element(By.CSS_SELECTOR, 'a.event__more')
    except Exception as error:
        logging.info('Não há mais sanfonas')

# Pega os jogos do ano
eventos = driver.find_elements(By.CSS_SELECTOR, 'div.event__match--twoLine')
links = []
for evento in eventos:
    link = evento.find_element(By.CSS_SELECTOR, 'a')
    links.append(link.get_attribute("href"))

logging.info('Iniciando coleta de dados')
for link in tqdm(links, total = len(links)):
    try:
        # Cria um conjunto de chaves que precisam ser preenchidas
        chaves_a_preencher = set(dados.keys())
        
        driver.get(link)
        time.sleep(1)

        chaves_a_preencher = set(dados.keys())
        # Pega os principais atributos
        nomesHA = driver.find_elements(By.CSS_SELECTOR, 'a.participant__participantName')
        nomeHome = nomesHA[0].text
        nomeAway = nomesHA[1].text
        hora = driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime')

        dados['HomeTeam'].append(nomeHome)
        dados['AwayTeam'].append(nomeAway)
        dados['DateTime'].append(hora.text)
        chaves_a_preencher.discard('HomeTeam')
        chaves_a_preencher.discard('AwayTeam')
        chaves_a_preencher.discard('DateTime')

        golsSpan = driver.find_element(By.CSS_SELECTOR, 'div.detailScore__wrapper')
        golSpan = golsSpan.find_elements(By.TAG_NAME, 'span')
        dados['FTHG'].append(golSpan[0].text)
        dados['FTAG'].append(golSpan[2].text)
        chaves_a_preencher.discard('FTHG')
        chaves_a_preencher.discard('FTAG')

        # Vai a seção Estatísticas
        navJogo = driver.find_elements(By.CSS_SELECTOR, 'div._tabsSecondary_myv7u_47')
        resultadoBotao = navJogo[0].find_elements(By.TAG_NAME, 'a')
        resultadoBotao[1].click()
        time.sleep(1)
        sections = driver.find_elements(By.CSS_SELECTOR, 'div._row_1nw75_8')

        for section in sections:
            section_text = section.find_element(By.CSS_SELECTOR, 'div._category_1ague_4').text
            if section_text in nomes:
                home_value = section.find_element(By.CSS_SELECTOR, 'div._homeValue_1jbkc_9').text
                away_value = section.find_element(By.CSS_SELECTOR, 'div._awayValue_1jbkc_13').text
                dados[nomes[section_text]['Home']].append(home_value)
                dados[nomes[section_text]['Away']].append(away_value)
                # Remove as chaves que foram preenchidas do conjunto
                chaves_a_preencher.discard(nomes[section_text]['Home'])
                chaves_a_preencher.discard(nomes[section_text]['Away'])

        # Preenche as chaves que não foram preenchidas com '-'
        for chave in chaves_a_preencher:
            dados[chave].append('-')

    except Exception as error:
        logging.error(f'\n Erro na coleta de dados: {error} \n No jogo {nomeHome} x {nomeAway}')


df = pd.DataFrame(dados)
filename = 'datasetFlashScore2022.csv'
df.to_csv(filename, sep = ';', index = False)
logging.info(f'Programa finalizado, aquivo CSV criado na pasta local, com o nome de {filename}')
