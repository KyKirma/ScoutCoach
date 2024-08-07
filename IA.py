import pandas as pd


df = pd.read_csv('datasetFlashScore.csv', delimiter= ';')
# Cria um atributo para o resultado do jogo, servindo como target da IA
resultado_jogo = []

for i in range(len(df['FTHG'])):
    if int(df['FTHG'][i]) > int(df['FTAG'][i]):
        resultado_jogo.append("Vitória do time da casa")
    elif int(df['FTHG'][i]) < int(df['FTAG'][i]):
        resultado_jogo.append("Vitória do time visitante")
    else:
        resultado_jogo.append("Empate")

df['Resultado'] = resultado_jogo
print(df)