import pickle
from ChampionSelectionModel import ChampionSelectionModel
from getGameMates import user

N_CHAMPIONS = 10

# 1. Importing the stats results
f = open('./data/champions-stats.Pickle', 'rb')
champions_stats = pickle.load(f)

# 2. Starting the approach with no bans and no selected champions
summonername = input("Entre com o Summoner Name: ")
MyUser = user(summonername)
print(MyUser)

pick = 0
role = 'mid'
gamemates = []
model = ChampionSelectionModel(summonername,pick,role,\
	gamemates,champions_stats,N_CHAMPIONS)

# 3. Collecting summoners info and match info
#model.getSummonersStats()
#bans = getBans()
#picks = getPicks()
#match_info = getMatchInfo()

# 4. Starting the champions graph with champions counter/strong
# information and the summoners statistics
model.start()
model.show_graph()

#####
# START OF THE EXPERIMENT
#####
# 5. Simulating the realtime champion selection
# a. bans
model.predict_bans()
model.update_bans(bans)
model.predict_picks()

# b. picks
for pick_round in range(6):
	print('Pick round',pick_round)
	model.update_pick()
	model.show()
####
# END OF THE EXPERIMENT
####

# 6. Evaluating the results for the match

# 8. Comparing the real result with the predicted result
