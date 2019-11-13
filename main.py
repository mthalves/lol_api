import pickle
from ChampionSelectionModel import ChampionSelectionModel

N_CHAMPIONS = 10

# 1. Importing the stats results
f = open('./data/champions-stats.Pickle','rb')
champions_stats = pickle.load(f)

# 2. Starting the approach with no bans and no selected champions
summonername = ''
gamemates = []
model = ChampionSelectionModel(summonername,pick,role,\
	gamemates,champions_stats,N_CHAMPIONS)

# 3. Collecting summoners info
#model.getSummonersStats()

# 4. Starting the analysis showing the first set for bans and picks
#model.start()
#model.show()

# 5. Collecting the match info
# bans =
# picks =
# match_info =

# 6. Simulating the realtime champion selection
# a. bans

# b. picks
for pick_round in range(6):
	print('Pick round',pick_round)
	#model.update()
	#model.show()

# 7. Evaluating the results for the match

# 8. Comparing the real result with the predicted result