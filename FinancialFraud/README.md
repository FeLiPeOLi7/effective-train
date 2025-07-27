# Financial Fraud Detection

Este projeto é um exemplo simples de detecção de fraudes financeiras usando Random Forest Classifier com ajuste para classe desbalanceada.
Utilizamos um dataset de transações financeiras, onde cada linha representa uma transação, e o objetivo é prever se ela é uma fraude (is_fraud = 1) ou não (is_fraud = 0).

# Objetivo

Prever se uma transação é ou não é fraude, a partir de informações anteriores.

# Observações

Pela natureza das fraudes serem muito raras, o modelo não consegue classificar tão bem, sendo então um problema do próprio dataset e da natureza dele.

Possuindo uma proporção para uma amostragem de 100.000 linhas de:

is_fraud
False    0.99762
True     0.00238

# Tecnologias Utilizadas

1. Pandas
2. Scikit-learn

# Referência
Kaggle (https://www.kaggle.com/datasets/aryan208/financial-transactions-dataset-for-fraud-detection)
