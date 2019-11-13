from bs4 import BeautifulSoup
import pandas as pd
import pickle
import re
import requests

from ChampionStat import ChampionStat

# 1. Openning the chapions list
result = []
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
		counter = {}
		table = soup.find('table', attrs={"class": "champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem"})
		tbody = table.find('tbody')
		td_c = tbody.find_all('td', attrs={"class": "champion-stats-header-matchup__table__champion"})
		td_w = tbody.find_all('td', attrs={"class": "champion-stats-header-matchup__table__winrate"})
		
		champions = []
		for data in td_c:
			champions.append(re.search("/>(.+?)\s*</td>",str(data)).group(1))

		winrate = []
		for data in td_w:
			winrate.append(re.search("<b>(.+?)</b>",str(data)).group(1))

		for i in range(len(champions)):
			counter[champions[i]] = winrate[i]
		print('|',counter)

		# d. strong against champion
		strong = {}
		table = soup.find('table', attrs={"class": "champion-stats-header-matchup__table champion-stats-header-matchup__table--weak tabItem"})
		tbody = table.find('tbody')
		td_c = tbody.find_all('td', attrs={"class": "champion-stats-header-matchup__table__champion"})
		td_w = tbody.find_all('td', attrs={"class": "champion-stats-header-matchup__table__winrate"})
		
		champions = []
		for data in td_c:
			champions.append(re.search("/>(.+?)\s*</td>",str(data)).group(1))

		winrate = []
		for data in td_w:
			winrate.append(re.search("<b>(.+?)</b>",str(data)).group(1))

		for i in range(len(champions)):
			strong[champions[i]] = winrate[i]
		print('|',strong)

		result.append(ChampionStat(champ_name,role,tier,counter,strong))
		
# 3. Saving the result
with open('./data/champions-stats.Pickle', 'wb') as output:  # Overwrites any existing file.
	pickle.dump(result, output, pickle.HIGHEST_PROTOCOL)