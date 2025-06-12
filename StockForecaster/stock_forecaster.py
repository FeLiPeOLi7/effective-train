from utils import create_stock_data, forecaster

def main():
    name, stock_data = create_stock_data()
    stock_data['Next_Close'] = stock_data['Close'].shift(-1)
    stock_data = stock_data.dropna()#Retirando a última linha
    predicted_close_value = forecaster(stock_data)

    print(f"O valor de fechamento da ação da empresa {name}, amanhã será de, {predicted_close_value[0]:.2f}")
    


if __name__ == "__main__":
    main() 