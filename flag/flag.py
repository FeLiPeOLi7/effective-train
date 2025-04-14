import requests
#from bs4 import BeautifulSoup as bs

flag = input("Put a flag of a country: ")
url = "https://restcountries.com/v3.1/name/"+flag

r = requests.get(url)
data = r.json()
#soup = bs(r.content, 'html.parser')

flagImage = data[0]["flags"]["png"]
print("Flag URL: ", flagImage)
