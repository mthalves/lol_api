import re

class ChampionStat:

	def __init__(self,name,role,tier,counter,strong):
		self.name = name
		self.role = role
		self.tier = tier
		self.counter = counter
		self.strong = strong

	def show(self):
		print('-----')
		print('|',self.name)
		print('-----')
		print('|',self.role)
		print('|',self.tier)
		print('|',self.counter)
		print('|',self.strong)
		print('-----')

def getChampion(champ_name,champion_stat):
	my_champ = formatChampionName(champ_name)
	for champ in champion_stat:
		# formating champion name
		champ_stat_name = formatChampionName(champ_name)
		if my_champ == champ_stat_name:
			return(champ)
	return(None)

def formatChampionName(champ_name):
	formated_champ_name = ''.join(c.lower() for c in champ_name if not c.isspace() and\
				 c != '&' and c != '\'' and c != ';')
	formated_champ_name = 'nunu' if re.match('nunu',formated_champ_name)\
									 is not None else formated_champ_name
	return formated_champ_name