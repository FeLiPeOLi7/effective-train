from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

''' 
    Recebe um dataframe com labels
    Retorna um dataframe com as colunas em formato numerico
'''
def convert_labels(df):
    #Lista de colunas a serem codificadas em formato numerico (modelo nao lida bem com texto)
    cols_to_encode = [
        'sender_account', 'receiver_account', 'transaction_type', 'merchant_category',
        'location', 'device_used', 'is_fraud',
        'payment_channel', 'ip_address', 'device_hash'
    ]

    #Para cada coluna faz um coluna codificada e a substitui
    for col in cols_to_encode:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    return df

def main():
    csv_path = 'financial_fraud_detection_dataset.csv'
    fin_data = pd.read_csv(csv_path, nrows=100000)

    print(fin_data['is_fraud'].value_counts(normalize=True))
    fin_data = convert_labels(fin_data)

    X = fin_data.drop(columns=['is_fraud', 'fraud_type', 'timestamp', 'transaction_id'])
    y = fin_data['is_fraud']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    clf = RandomForestClassifier(class_weight='balanced')
    clf.fit(X_train, y_train)
    
    np.set_printoptions(threshold=np.inf)
    print(clf.predict(X_test))



if __name__ == '__main__':
    main()