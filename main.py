import csv
import pickle

import matplotlib.pyplot as plt

from ChampionSelectionModel import ChampionSelectionModel
from ChampionStat import *
from getGameMates import user

N_CHAMPIONS = 10

def getBans(match_info):
	bans = [match_info[i] for i in range(3,13)]
	return(bans)

def getPicks(match_info):
	picks = [match_info[(i*5)+13] for i in range(10)]
	return(picks)

def getLanes(match_info):
	picks = [match_info[(i*5)+14] for i in range(10)]
	return(picks)

def getSummoners(match_info):
	summoners = [match_info[(i*5)+15] for i in range(10)]
	return(summoners)

def getVictory(match_info):
	return(True if match_info[-1] == 'True' else False)

def getRole(lane,pick):
	global champions_stats

	if lane == 'BOTTOM':
		champion = getChampion(pick,champions_stats)
		if champion.role == 'Bottom':
			return('BOTTOM')
		else:
			return('SUPPORT')
	else:
		return(lane)

def getGameMates(main,summoners,lanes,picks):
	main_idx = summoners.index(main)
	if main_idx < 5:
		gamematesname = [summoners[i] for i in range(0,5) if i != main_idx]
		gamemateslane = [lanes[i] for i in range(0,5) if i != main_idx]
		gamematespick = [picks[i] for i in range(0,5) if i != main_idx]
	else:
		gamematesname = [summoners[i] for i in range(5,10) if i != main_idx]
		gamemateslane = [lanes[i] for i in range(5,10) if i != main_idx]
		gamematespick = [picks[i] for i in range(5,10) if i != main_idx]

	gamemates = []
	for i in range(0,4):
		gamemates.append([\
			gamematesname[i],\
			getRole(gamemateslane[i], gamematespick[i])])

	return(gamemates)

# 1. Importing the stats results
f = open('./data/champions-stats.Pickle', 'rb')
champions_stats = pickle.load(f)

# 2. Starting the approach with no bans and no selected champions
result_file = open('results.csv','w+')
result_file.write('GoodBans1'+';'+'GoodBans2'\
					+';'+'GoodPicks1'+';'+'GoodPicks2'+';'+'Victory\n')
result_file.close()

counter = 0
number_of_matches = len(open('data/match-list.csv','r').readlines())
with open('data/match-list.csv','r') as csv_file:
	counter += 1
	csvreader = csv.reader(csv_file) 
	next(csvreader) # ignoring header

	print('Running Match '+str(counter)+'/'+str(number_of_matches))
	for match_info in csvreader:
		bans_results = []
		picks_results = []

		# 3. Getting match general information
		summoners = getSummoners(match_info)
		bans = getBans(match_info)
		picks = getPicks(match_info)
		lanes = getLanes(match_info)
		victory = getVictory(match_info)

		# 4. Running estimation for each summoner
		predicted_bans1 = set()
		predicted_bans2 = set()
		team1_picks, team2_picks = 0, 0
		for k in range(len(summoners)):
			entropy = []
			# a. getting main summoner start information
			summonername = summoners[k]
			pick = picks[k]
			pick_order = k
			role = getRole(lanes[k],picks[k])
			gamemates = getGameMates(summonername,summoners,lanes,picks)

			print('=====\n> Estimation for summoner',k+1,':',summonername,'('+role+')')

			# b. initializing and starting/updating the model with
			# current information
			model = ChampionSelectionModel(summonername,pick_order,role,\
				gamemates,champions_stats,N_CHAMPIONS)
			model.start()
			entropy.append(model.get_entropy())

			#model.plot_graph('network.pdf')
			#model.plot_nodes_degree('degree.pdf')
			#print('Shanon Entropy:',model.get_entropy())
			#model.plot_local_cluster('local_cluster.pdf')
			#print('Transitivity (Global Cluster):',model.get_global_cluster())
			
			#####
			# START OF THE EXPERIMENT
			#####
			# 5. Simulating the realtime champion selection
			# a. BANS
			# i. predicting the bans
			p_bans = model.predict_bans()
			entropy.append(model.get_entropy())
			#print(p_bans)

			# ii. adding the bans to the team set
			if k < 5:
				for ban in p_bans:
					predicted_bans1.add(ban)
			else:
				for ban in p_bans:
					predicted_bans2.add(ban)

			# iii. updating bans and removing champions 
			# node in the graph
			if k < 5:
				model.update_bans(bans)

			# b. PICKS
			# i. predicting the first picks
			predicted_picks = model.predict_picks(0)
			#print(predicted_picks)
			#model.plot_nodes_visits('Visit_1.pdf')

			# ii. simulating the picks phase
			team1_counter, team2_counter = 0, 0
			for pick_round in range(6):
				# picking
				if pick_round == 0:
					model.update_pick(picks[team1_counter],k < 5)
					team1_counter += 1
				elif pick_round == 5:
					model.update_pick(picks[5+team2_counter],k >= 5)
					team2_counter += 1
				else:
					if team1_counter < team2_counter:
						model.update_pick(picks[team1_counter],k < 5)
						model.update_pick(picks[team1_counter+1],k < 5)
						team1_counter += 2
					else:
						model.update_pick(picks[5+team2_counter],k >= 5)
						model.update_pick(picks[5+team2_counter+1],k >= 5)
						team2_counter += 2

				# checking stop condition (already pick)
				#print('|Team 1 Picks =',team1_counter,\
				#	'x',team2_counter,'= Team 2 Picks')
				if k < 5:
					if (k % 5) < team1_counter:
						if pick in predicted_picks:
							team1_picks += 1
						break
				else:
					if (k % 5) < team2_counter:
						if pick in predicted_picks:
							team2_picks += 1 
						break

				# updating the model
				predicted_picks = model.predict_picks(pick_round+1)
				entropy.append(model.get_entropy())
				#print(predicted_picks)
				#model.plot_nodes_visits('Visit_'+str(pick_round+2)+'.pdf')

			# iii. plotting model entropy
			#plt.plot(entropy, '-', linewidth=2, markersize=12)
			#plt.ylabel('Entropy', fontsize=20)
			#plt.show()
			####
			# END OF THE EXPERIMENT
			####

		# 6. Evaluating the results for the match
		# a. BANS
		team1_bans, counter1 = 0, 0
		for ban in bans[0:5]:
			if ban != '':
				counter1 += 1
				if (ban in predicted_bans1 and victory)\
				or (ban not in predicted_bans1 and not victory):
					team1_bans += 1

		team2_bans, counter2 = 0, 0
		for ban in bans[5:10]:
			if ban != '':
				counter2 += 1
				if (ban in predicted_bans2 and victory)\
				or (ban not in predicted_bans2 and not victory):
					team2_bans += 1

		#print('| BANS RESULT:')
		#print('| Good bans (Team 1):',team1_bans/counter1 ,'- Win?',victory)
		#print('| Good bans (Team 2):',team2_bans/counter2 ,'- Win?',not victory)
		bans_results = [team1_bans/counter1,team2_bans/counter2,victory]

		# b. PICKS
		#print('| PICKS RESULT:')
		#print('| Good picks (Team 1):',team1_picks/5 ,'- Win?',victory)
		#print('| Good picks (Team 2):',team2_picks/5 ,'- Win?',not victory)
		picks_results = [team1_picks/5,team2_picks/5,victory]

		# 7. Saving the result
		result_file = open('results.csv','a')
		result_file.write(str(bans_results[0])+';'+str(bans_results[1])\
							+';'+str(picks_results[0])+';'+str(picks_results[1])+';'+str(victory)+'\n')
		result_file.close()
