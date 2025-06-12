import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def create_stock_data():
    try:
        ticker_name = input("Digite aqui o ticket da empresa na Bolsa de Valores que você quer prever: ")
        stock = yf.Ticker(ticker_name)
        company_name = stock.info['longName']
        stock_data = stock.history(period='max')

        df = pd.DataFrame(stock_data)
    except:
        print("\nEssa empresa não está listada na bolsa de valores!")
        company_name, df = create_stock_data()

    
    return company_name, df

def forecaster(stock_data):
    X = stock_data.drop(columns=["Next_Close"]) #O que nosso modelo vai usar para aprender, exceto o rotulo, que 
    y = stock_data["Next_Close"] #o que nosso modelo vai precisar prever, no caso, o grau do acidente

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    reg = LinearRegression()
    reg.fit(X_train, y_train)

    stock = stock_data.iloc[-1:].drop(columns=['Next_Close'])

    return reg.predict(stock)