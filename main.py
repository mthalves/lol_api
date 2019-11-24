import csv
import pickle

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
			return('ADC')
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
with open('data/match-list.csv','r') as csv_file:
	csvreader = csv.reader(csv_file) 
	next(csvreader) # ignoring header

	for match_info in csvreader:
		# 3. Getting match general information
		summoners = getSummoners(match_info)
		bans = getBans(match_info)
		picks = getPicks(match_info)
		lanes = getLanes(match_info)
		victory = getVictory(match_info)

		# 4. Running estimation for each summoner
		for k in range(len(summoners)):
			# a. getting main summoner start information
			summonername = summoners[k]
			pick = picks[k]
			pick_order = k
			role = getRole(lanes[k],picks[k])
			gamemates = getGameMates(summonername,summoners,lanes,picks)

			print('Estimation for summoner',k+1,':',summonername,'('+role+')')

			# b. initializing and starting/updating the model with
			# current information
			model = ChampionSelectionModel(summonername,pick_order,role,\
				gamemates,champions_stats,N_CHAMPIONS)
			model.start()
			exit(1)

			#model.show_graph()
			#model.show_nodes_degree()
			#print('Shanon Entropy:',model.get_entropy())
			#model.show_local_cluster()
			#print('Transitivity (Global Cluster):',model.get_global_cluster())

			#####
			# START OF THE EXPERIMENT
			#####
			# 5. Simulating the realtime champion selection
			# a. bans
			#model.predict_bans()
			#model.update_bans(bans)
			#model.predict_picks()

			# b. picks
			#for pick_round in range(6):
			#	print('Pick round',pick_round)
			#	model.update_pick()
			#	model.show()
			####
			# END OF THE EXPERIMENT
			####

			# 6. Evaluating the results for the match

			# 8. Comparing the real result with the predicted result
