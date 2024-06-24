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
options.add_experimental_option('detach', True)

# Criando o driver "bot"
driver = webdriver.Chrome(options=options)

# Bibliotecas extras
import time
import pandas as pd
from tqdm import tqdm

driver.get("https://www.flashscore.com.br/futebol/brasil/brasileirao-betano/resultados/") 
time.sleep(2)

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

# Pega os jogos do ano
eventos = driver.find_elements(By.CSS_SELECTOR, 'div.event__match--twoLine')
links = []
for evento in eventos:
    link = evento.find_element(By.CSS_SELECTOR, 'a')
    links.append(link.get_attribute("href"))

for link in tqdm(links, total = len(links)):
    try:
        driver.get(link)
        time.sleep(1)

        # Pega os principais atributos
        nomes = driver.find_elements(By.CSS_SELECTOR, 'a.participant__participantName')
        nomeHome = nomes[0].text
        nomeAway = nomes[1].text
        hora = driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime')

        dados['HomeTeam'].append(nomeHome)
        dados['AwayTeam'].append(nomeAway)
        dados['DateTime'].append(hora.text)

        golsSpan = driver.find_element(By.CSS_SELECTOR, 'div.detailScore__wrapper')
        golSpan = golsSpan.find_elements(By.TAG_NAME, 'span')
        dados['FTHG'].append(golSpan[0].text)
        dados['FTAG'].append(golSpan[2].text)

        # Vai a seção Estatísticas
        navJogo = driver.find_elements(By.CSS_SELECTOR, 'div._tabs_i2rza_4')
        resultadoBotao = navJogo[1].find_elements(By.TAG_NAME, 'a')
        resultadoBotao[1].click()
        time.sleep(1)

        sections = driver.find_elements(By.CSS_SELECTOR, 'div._row_bn1w5_8')

        # Correção caso haja section de Gols Esperados e Cartões Vermelhos
        if sections[0].find_element(By.CSS_SELECTOR, 'div._category_hyte3_4').text != 'Gols Esperados (xG)': # Se não houver a sessão 'Gols esperados'
            i = 0
            dados['HGE'].append("-")
            dados['AGE'].append("-")

            if sections[11].find_element(By.CSS_SELECTOR, 'div._category_hyte3_4').text == 'Cartões Vermelhos': # E a sessão 'Cartões vermelhos' existir
                j = 1 
                HCV = sections[11].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *PB = Posse de Bola
                ACV = sections[11].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
                dados['HCV'].append(HCV.text)
                dados['ACV'].append(ACV.text)
            else:
                dados['HCV'].append(0)
                dados['ACV'].append(0)
                j = 0

        else: # Se tive a sessão 'Gols esperados'

            if sections[12].find_element(By.CSS_SELECTOR, 'div._category_hyte3_4').text == 'Cartões Vermelhos': # E a sessão 'Cartões vermelhos' existir
                j = 1   
                HCV = sections[12].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *PB = Posse de Bola
                ACV = sections[12].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
                dados['HCV'].append(HCV.text)
                dados['ACV'].append(ACV.text)
            else:
                dados['HCV'].append(0)
                dados['ACV'].append(0)
                j = 0

            i = 1
            HGE = sections[0].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *GE = Gols Esperado
            AGE = sections[0].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
            dados['HGE'].append(HGE.text)
            dados['AGE'].append(AGE.text)
        
        HPB = sections[0 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *PB = Posse de Bola
        APB = sections[0 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HPB'].append(HPB.text)
        dados['APB'].append(APB.text)

        HTG = sections[1 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *GT = Tentativa de Gol
        ATG = sections[1 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HTG'].append(HTG.text)
        dados['ATG'].append(ATG.text)

        HCG = sections[2 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *CG = Chutes no Gol
        ACG = sections[2 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HCG'].append(HCG.text)
        dados['ACG'].append(ACG.text)

        HCF = sections[3 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *CF = Chutes para Fora
        ACF = sections[3 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HCF'].append(HCF.text)
        dados['ACF'].append(ACF.text)

        HCB = sections[4 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *CB = Chutes Bloqueados
        ACB = sections[4 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HCB'].append(HCB.text)
        dados['ACB'].append(ACB.text)

        HFC = sections[5 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *FC = Faltas Cobradas
        AFC = sections[5 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HFC'].append(HFC.text)
        dados['AFC'].append(AFC.text)

        HES = sections[6 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *ES = Escanteios
        AES = sections[6 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HES'].append(HES.text)
        dados['AES'].append(AES.text)

        HIP = sections[7 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *IP = Impedimentos
        AIP = sections[7 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HIP'].append(HIP.text)
        dados['AIP'].append(AIP.text)

        HLC = sections[8 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *LC = Laterais Cobradas
        ALC = sections[8 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HLC'].append(HLC.text)
        dados['ALC'].append(ALC.text)

        HDG = sections[9 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *DG = Defesas do Goleiro
        ADG = sections[9 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HDG'].append(HDG.text)
        dados['ADG'].append(ADG.text)

        HFT = sections[10 + i].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *FT = Faltas
        AFT = sections[10 + i].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HFT'].append(HFT.text)
        dados['AFT'].append(AFT.text)

        HCA = sections[11 + i + j].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *CA = Cartões Amarelos
        ACA = sections[11 + i + j].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HCA'].append(HCA.text)
        dados['ACA'].append(ACA.text)

        HPT = sections[12 + i + j].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *PT = Passes Totais
        APT = sections[12 + i + j].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HPT'].append(HPT.text)
        dados['APT'].append(APT.text)

        HPC = sections[13 + i + j].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *PC = Passes Completos
        APC = sections[13 + i + j].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HPC'].append(HPC.text)
        dados['APC'].append(APC.text)

        HATK = sections[14 + i + j].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *ATK = Ataques
        AATK = sections[14 + i + j].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HATK'].append(HATK.text)
        dados['AATK'].append(AATK.text)

        HATKP = sections[15 + i + j].find_element(By.CSS_SELECTOR, 'div._homeValue_lgd3g_9') # *ATKP = Ataques Perigosos
        AATKP = sections[15 + i + j].find_element(By.CSS_SELECTOR, 'div._awayValue_lgd3g_13')
        dados['HATKP'].append(HATKP.text)
        dados['AATKP'].append(AATKP.text)

    except Exception as error:
        print(f'ERRO PEDRO OKLHA AQUI: {error}')

df = pd.DataFrame(dados)
filename = 'datasetFlashScore.csv'
df.to_csv(filename, sep = ';', index = False)