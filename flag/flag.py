import requests
from bs4 import BeautifulSoup as bs

flag = input("Put a flag of a country: ")
url = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"+'q='+flag
r = requests.get(url)
soup = bs(r.content, 'html.parser')
flagImage = soup.find_all('img', {'class': 'rg_i Q4LuWd'})['scr']
print(flagImage)
