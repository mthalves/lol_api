import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

# 1. Openning the chapions list
with open('./data/champions-list.csv','r') as f:
	for line in f:
		# 2. Retriving the champion's name statistics page
		champ_name = line[:-1]
		req = requests.get('https://br.op.gg/champion/'+\
			''.join(c.lower() for c in champ_name if not c.isspace())+'/statistics')
		if req.status_code == 200:
			print('Successful Request for '+champ_name+'!')
			content = req.content
			#print(content.prettify())

		# 3. Getting the information
		# a. role
		soup = BeautifulSoup(content, 'html.parser')
		span = soup.find('span', attrs={"class": "champion-stats-header__position__role"})
		role = re.search(">(.+?)</span>",str(span)).group(1)
		print('| Role:',role)

		# b. tier
		soup = BeautifulSoup(content, 'html.parser')
		div = soup.find('div', attrs={"class": "champion-stats-header-info__tier"})
		tier = re.search("<b>Tier (.+?)</b>",str(div)).group(1)
		print('| Tier:',tier)

		# c. counter champion
		table = soup.find('table', attrs={"class": "champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem"})
		tbody = table.find('tbody')
		td = tbody.find_all('td')
		for data in td:
			print(data)
		exit(1)
