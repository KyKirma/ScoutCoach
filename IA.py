import pandas as pd
df1 = pd.read_csv('Database/datasetFlashScore.csv', delimiter=';')
df2 = pd.read_csv('Database/datasetFlashScore2022.csv', delimiter=';')

# Concatena os dois dataframes
df = pd.concat([df1, df2], ignore_index = True)

# Cria um atributo para o resultado do jogo, servindo como target da IA
df['Resultado'] = df.apply(lambda row: "Vitória do time da casa" if int(row['FTHG']) > int(row['FTAG']) else "Vitória do time visitante" if int(row['FTHG']) < int(row['FTAG']) else "Empate", axis=1)

# Cria uma coluna para indicar se o jogo teve 3 gols ou mais
df['Over 2.5'] = df.apply(lambda row: 1 if int(row['FTHG']) + int(row['FTAG']) >= 3 else 0, axis=1)
df = df.drop(columns=['FTAG', 'FTHG'])
dfTestes = df.head(20)
dfTreinamento = df.iloc[20:]

from pycaret.classification import *
s = setup(dfTreinamento, target = 'Over 2.5', session_id = 123)

best = compare_models()

tuned = tune_model(best)

predictions = predict_model(tuned, data=dfTestes, raw_score = True)



