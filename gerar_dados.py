from ucimlrepo import fetch_ucirepo

heart = fetch_ucirepo(id=45)
dados = heart.data.features.copy()
dados["doenca"] = (heart.data.targets.iloc[:, 0] > 0).astype(int)
dados.to_csv("heart.csv", index=False)
print(dados.shape)