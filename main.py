import pickle
from ChampionSelectionModel import ChampionSelectionModel

N_CHAMPIONS = 10
TOURNAMENT = False

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
model.start()
model.show()

# 5. Collecting the match info
# bans = getBans()
# picks = getPicks()
# match_info = getMatchInfo()

# 6. Simulating the realtime champion selection
# a. bans
if TOURNAMENT:
	for i in range(10):
		if i == model.pick_order:
			predict_bans()
			model.update_single_ban(bans[i])
		else:
			model.update_single_ban(bans[i])
else:
	model.predict_bans()
	model.update_bans(bans)
	model.predict_picks()

# b. picks
for pick_round in range(6):
	print('Pick round',pick_round)
	model.update_pick()
	model.show()

# 7. Evaluating the results for the match

# 8. Comparing the real result with the predicted result