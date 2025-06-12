import pandas as pd
from newsapi import NewsApiClient
from key import my_api_key
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import re
import unicodedata

class Indicators:
    FEAR = "MEDO"
    FEAR_LIST = ["queda", "crash", "recessão", "cair", "morreu", "acabou", "risco", "desvalorização", "pânico", "insegurança", "baixa", "desastre", "venda", "bear"]
    GREED = "OTIMISTA"
    GREED_LIST = ["alta", "valorização", "subir", "recorde", "lucro", "crescimento", "oportunidade", "expansão", "confiança", "compra", "bull"]
    NEUTRAL = "NEUTRO"

def clean_text(text):
    # Remove pontuações e acentos, transforma em minúsculas
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def label_text(text, greed_list, fear_list):
    greed = 0
    fear = 0
    cleaned_text = clean_text(text)
    for word in cleaned_text.split():
        if word in greed_list:
            greed += 1
        elif word in fear_list:
            fear += 1
    
    if greed > fear:
        return Indicators.GREED
    elif fear > greed:
        return Indicators.FEAR
    else:
        return Indicators.NEUTRAL


def sentiment_analysis(data_frame):
    
    contents = data_frame['content'].fillna('').values.tolist()
    titles = data_frame['title'].fillna('').values.tolist()
    texts = contents + titles #train_x

    # Adiciona manualmente textos com palavras relevantes, pois somente as notícias não são suficientes
    texts.extend([
        "O Bitcoin vai explodir em breve, uma grande alta vem aí",     # OTIMISTA
        "Compre agora antes da valorização",                            # OTIMISTA
        "O mercado está em pânico com a queda",                         # MEDO
        "Desvalorização forte causa insegurança entre investidores",    # MEDO
        "O Bitcoin morreu", #MEDO
        "O Bitcoin irá cair, venda rápido", #MEDO
    ])

    vectorizer = CountVectorizer()
    train_x_vectors = vectorizer.fit_transform(texts)

    train_y = []
    for text in texts:
        train_y.append(label_text(text, Indicators.GREED_LIST, Indicators.FEAR_LIST))


    clf_svm = svm.SVC(kernel='linear')
    clf_svm.fit(train_x_vectors, train_y)


    # Predição
    news_texts = [clean_text(c + " " + t) for c, t in zip(contents, titles)]
    news_vectors = vectorizer.transform(news_texts)
    predictions = clf_svm.predict(news_vectors)

    # Contagem
    from collections import Counter
    counts = Counter(predictions)

    print("\nClassificação das notícias:")
    for key, value in counts.items():
        print(f"{key}: {value}")

    # Veredito final
    fear = counts.get(Indicators.FEAR, 0)
    greed = counts.get(Indicators.GREED, 0)
    neutro = counts.get(Indicators.NEUTRAL, 0)

    if (greed > fear) and neutro < greed:
        print("\n🟢 VEREDITO FINAL: O mercado está OTIMISTA.")
    elif (fear > greed) and neutro < fear:
        print("\n🔴 VEREDITO FINAL: O mercado está com MEDO.")
    else:
        print("\n🟡 VEREDITO FINAL: O mercado está NEUTRO.")
    