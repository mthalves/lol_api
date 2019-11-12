import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Requesting the OPGG Home Page
req = requests.get('https://br.op.gg/champion/statistics')
if req.status_code == 200:
	print('Successful Request!')
	content = req.content
	#print(content.prettify())

# 2. Recovering Champions's name list
result = []
soup = BeautifulSoup(content, 'html.parser')
dl = soup.find_all('div', attrs={"class": "champion-index__champion-item__name"})
for d in dl:
	name = str(d).split('>')[1]
	name = name.split('<')[0]
	result.append(name)

# 3. Saving the result into csv file
f = open('./data/champions-list.csv','w')
for champ in result:
	f.write(champ+'\n')
f.close()