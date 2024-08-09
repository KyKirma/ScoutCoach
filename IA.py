import pandas as pd

# Lê os dois dataframes
df1 = pd.read_csv('datasetFlashScore.csv', delimiter=';')
df2 = pd.read_csv('datasetFlashScore2022.csv', delimiter=';')

# Concatena os dois dataframes
df = pd.concat([df1, df2])

# Cria um atributo para o resultado do jogo, servindo como target da IA
df['Resultado'] = df.apply(lambda row: "Vitória do time da casa" if int(row['FTHG']) > int(row['FTAG']) else "Vitória do time visitante" if int(row['FTHG']) < int(row['FTAG']) else "Empate", axis=1)

# Cria uma coluna para indicar se o jogo teve 3 gols ou mais
df['Over 2.5'] = df.apply(lambda row: 1 if int(row['FTHG']) + int(row['FTAG']) >= 3 else 0, axis=1)

print(df)