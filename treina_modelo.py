from ucimlrepo import fetch_ucirepo

heart_disease = fetch_ucirepo(id=45)
dados = heart_disease.data.features

dados["doenca"] = (heart_disease.data.targets > 0) * 1

x = dados.drop(columns = 'doenca')
y = dados['doenca']

from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state = 432, stratify = y)

import xgboost as xgb
modelo = xgb.XGBClassifier(objective='binary:logistic')
modelo.fit(train_x, train_y)
preds = modelo.predict(test_x)

from sklearn.metrics import accuracy_score
acuracia = accuracy_score(test_y, preds)
print(f'A acurácia do modelo é {acuracia:.2%}')

import joblib
joblib.dump(modelo, 'modelo_xgboost.pkl')

#caso o usuario não possua todos os dados a serem fornecidos, o modelo usará a media deles
medianas = x.median()
joblib.dump(medianas, 'medianas.pkl')

#modelo para a acurácia
previsoes = modelo.predict(test_x)
acuracia = accuracy_score(test_y, previsoes)

joblib.dump({'acuracia': acuracia}, 'metricas.pkl')
