from utils import sentiment_analysis
import pandas as pd
from newsapi import NewsApiClient
from key import my_api_key


def main():
    newsapi = NewsApiClient(api_key=my_api_key)

    data = newsapi.get_everything(q='bitcoin', language='pt', sort_by='relevancy', page=2)
    
    df = pd.DataFrame(data['articles'])
    sentiment_analysis(df)
    
if __name__ == "__main__":
    main()