import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

csv_path = "industrial_accidents_in_brazil_from_news.csv" #Dataset disponivel em https://www.kaggle.com/datasets/lhucastenorio/industrial-accidents-brazil-from-news-2011-2023

df = pd.read_csv(csv_path)

#Lista de colunas a serem codificadas em formato numerico (modelo nao lida bem com texto)
cols_to_encode = [
    'estado', 'cidade', 'area_da_industria', 'area_especifica',
    'cod_CNAE', 'processo', 'processo_especifico',
    'evento', 'evento_especifico'
]

#Para cada coluna faz um coluna codificada e a substitui
for col in cols_to_encode:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col]) 


X = df.drop(columns=["grau", "url"]) #O que nosso modelo vai usar para aprender, exceto o rotulo, que 
y = df["grau"] #o que nosso modelo vai precisar prever, no caso, o grau do acidente

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=1.0))#1.0 para não dar nenhum warning



'''

O código abaixo tem a intenção de testar o modelo, utilizando um acidente fictício que deveria ser grave

'''


# Novo acidente 
novo_acidente = {
    'estado': 'SP',
    'cidade': 'São Paulo',
    'area_da_industria': 'Metalurgia',
    'area_especifica': 'Siderurgia',
    'cod_CNAE': 'C10',
    'processo': 'Fusão',
    'processo_especifico': 'Fusão Elétrica',
    'evento': 'Explosão',
    'evento_especifico': 'Explosão de Caldeira',
    'vitimas': 34,
    'fatalidades': 3,
    'mes': 2,
    'ano': 2021,
}

novo_df = pd.DataFrame([novo_acidente])

for new_cols in cols_to_encode:
    le = LabelEncoder()
    novo_df[new_cols] = le.fit_transform(novo_df[new_cols])

# Fazer a previsão com o modelo treinado
grau_previsto = clf.predict(novo_df)

print("Grau previsto do acidente:", grau_previsto[0])