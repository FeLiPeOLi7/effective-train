import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Carrega o dataset produzido anteriormente com os emails da pessoa
data = pd.read_csv('emails_extended.csv')

# Extrai do dataset colunas importantes
X = data['Body']  # Input: Email original
y = data['ResponseBody']  # Output: Resposta esperada

# Divide o dataset entre treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Transforma o texto em números para facilitar o treinamento
pipeline = make_pipeline(CountVectorizer(), MultinomialNB())

# Treina o modelo
pipeline.fit(X_train, y_train)

# Da uma nota para o modelo
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisao do Modelo: {accuracy}')

# Salva o model treinado
joblib.dump(pipeline, 'email_responder_model.pkl')