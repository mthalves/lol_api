import requests
import pandas as pd
import numpy.random as rd

"""
Request from API
params:
URL: link to request
PARAMS: dictonary with request header
"""
def __FetchAPI(URL, PARAMS = {}):
	try:
		return requests.get(url=URL, params=PARAMS).json()
	except:
		print("Bad request")

"""
Request from Match
params:
Id: id for match
API_key: key to acess data information ate riotgames api
"""
def __FetchMatch(matchId, API_KEY):
	URL = "https://br1.api.riotgames.com/lol/match/v4/matches/" + str(matchId)
	PARAMS = {'api_key': API_KEY}

	return __FetchAPI(URL, PARAMS)

def __FetchMatchList(accountId, API_KEY):
	URL = "https://br1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(accountId) + "?queue=440&queue=420"
	PARAMS = {'api_key': API_KEY}

	return __FetchAPI(URL, PARAMS)
"""
Request a chapion ID Hash from ddragon LoL api
"""
def ChampionIdHash():
	URL = "http://ddragon.leagueoflegends.com/cdn/9.23.1/data/en_US/champion.json"
	champData = __FetchAPI(URL)
	champData = champData["data"]
	champHash = {}
	
	for champion in champData:
		champHash[int(champData[champion]["key"])] = champion 

	return champHash

"""
convert champion id to champion name
params:
id: champion id
champHash: championHash (given by ddragon api)
"""

def ChampId2Name(id, champHash):
	if id < 0:
		return None
	else:
		return champHash[id]


"""
Get data from game mode, bans, picks and lanes from a given matchId
params:
matchId: id for match
API_KEY: the acess Key for riot games API
champHas: the Hash identifier for champions
"""
def FetchMatchData(matchId, API_KEY, champHash):
	data = __FetchMatch(matchId, API_KEY)


	try:

		if data["queueId"] == 420:
			gameMode = "Ranked-5v5-Solo"
		elif data["queueId"] == 440:
			gameMode = "Ranked-5v5-Flex"
		else:
			print("Not a Ranked queue.")
			return None

		game_result = data["teams"][0]["win"] == "Win"
		row = { "matchId": 	data["gameId"],
				"gameMode": gameMode, 
				"ban1": ChampId2Name(data["teams"][0]["bans"][0]["championId"], champHash),
				"ban2": ChampId2Name(data["teams"][0]["bans"][1]["championId"], champHash),
				"ban3": ChampId2Name(data["teams"][0]["bans"][2]["championId"], champHash),
				"ban4": ChampId2Name(data["teams"][0]["bans"][3]["championId"], champHash),
				"ban5": ChampId2Name(data["teams"][0]["bans"][4]["championId"], champHash),
				"ban6": ChampId2Name(data["teams"][1]["bans"][0]["championId"], champHash),
				"ban7": ChampId2Name(data["teams"][1]["bans"][1]["championId"], champHash),
				"ban8": ChampId2Name(data["teams"][1]["bans"][2]["championId"], champHash),
				"ban9": ChampId2Name(data["teams"][1]["bans"][3]["championId"], champHash),
				"ban10": ChampId2Name(data["teams"][1]["bans"][4]["championId"], champHash),
				"champ1": ChampId2Name(data["participants"][0]["championId"], champHash),
				"lane1": data["participants"][0]["timeline"]["lane"],
				"Name1": data["participantIdentities"][0]["player"]["summonerName"],
				"summonerId1": data["participantIdentities"][0]["player"]["summonerId"],
				"accountId1": data["participantIdentities"][0]["player"]["accountId"],
				"champ2": ChampId2Name(data["participants"][1]["championId"], champHash),
				"lane2": data["participants"][1]["timeline"]["lane"],
				"Name2": data["participantIdentities"][1]["player"]["summonerName"],
				"summonerId2": data["participantIdentities"][1]["player"]["summonerId"],
				"accountId2": data["participantIdentities"][1]["player"]["accountId"],
				"champ3": ChampId2Name(data["participants"][2]["championId"], champHash),
				"lane3": data["participants"][2]["timeline"]["lane"],
				"Name3": data["participantIdentities"][2]["player"]["summonerName"],
				"summonerId3": data["participantIdentities"][2]["player"]["summonerId"],
				"accountId3": data["participantIdentities"][2]["player"]["accountId"],
				"champ4": ChampId2Name(data["participants"][3]["championId"], champHash),
				"lane4": data["participants"][3]["timeline"]["lane"],
				"Name4": data["participantIdentities"][3]["player"]["summonerName"],
				"summonerId4": data["participantIdentities"][3]["player"]["summonerId"],
				"accountId4": data["participantIdentities"][3]["player"]["accountId"],
				"champ5": ChampId2Name(data["participants"][4]["championId"], champHash),
				"lane5": data["participants"][4]["timeline"]["lane"],
				"Name5": data["participantIdentities"][4]["player"]["summonerName"],
				"summonerId5": data["participantIdentities"][4]["player"]["summonerId"],
				"accountId5": data["participantIdentities"][4]["player"]["accountId"],
				"champ6": ChampId2Name(data["participants"][5]["championId"], champHash),
				"lane6": data["participants"][5]["timeline"]["lane"],
				"Name6": data["participantIdentities"][5]["player"]["summonerName"],
				"summonerId6": data["participantIdentities"][5]["player"]["summonerId"],
				"accountId6": data["participantIdentities"][5]["player"]["accountId"],
				"champ7": ChampId2Name(data["participants"][6]["championId"], champHash),
				"lane7": data["participants"][6]["timeline"]["lane"],
				"Name7": data["participantIdentities"][6]["player"]["summonerName"],
				"summonerId7": data["participantIdentities"][6]["player"]["summonerId"],
				"accountId7": data["participantIdentities"][6]["player"]["accountId"],
				"champ8": ChampId2Name(data["participants"][7]["championId"], champHash),
				"lane8": data["participants"][7]["timeline"]["lane"],
				"Name8": data["participantIdentities"][7]["player"]["summonerName"],
				"summonerId8": data["participantIdentities"][7]["player"]["summonerId"],
				"accountId8": data["participantIdentities"][7]["player"]["accountId"],
				"champ9": ChampId2Name(data["participants"][8]["championId"], champHash),
				"lane9": data["participants"][8]["timeline"]["lane"],
				"Name9": data["participantIdentities"][8]["player"]["summonerName"],
				"summonerId9": data["participantIdentities"][8]["player"]["summonerId"],
				"accountId9": data["participantIdentities"][8]["player"]["accountId"],
				"champ10": ChampId2Name(data["participants"][9]["championId"], champHash),
				"lane10": data["participants"][9]["timeline"]["lane"],
				"Name10": data["participantIdentities"][9]["player"]["summonerName"],
				"summonerId10": data["participantIdentities"][9]["player"]["summonerId"],
				"accountId10": data["participantIdentities"][9]["player"]["accountId"],
				"team1win": game_result}

		return row

	


	except KeyError:
		print("Error: " + str(data["status"]["status_code"]) + ". Reason: " + data["status"]["message"])
	except :
		print("Bad Request")

"""
Brute Force Crawler for match information
params:
initialId: id in which the search will begain
API_KEY
N: number of id to search from
"""
def MatchCrawler(initialId, API_KEY, N, M):
	print("Retriving Champion ID data...")
	champDict = ChampionIdHash()
	dataList = []
	print("Retriving matches data:")
	
	matchId = initialId
	for j in range(0, M):
		for i in range(0, N):
			print("Retriving matcheId: %d, (%d*%d)" % (matchId, i, j))
			row = FetchMatchData(matchId, API_KEY, champDict)
			if row != None:
				dataList.append(row)
				
				#random last 3 games
				nextParticipantId = rd.randint(1, 11)

				readable = False
				while not readable:
					nextAccountId = row["accountId"+ str(nextParticipantId)]
					matchlists = __FetchMatchList(nextAccountId, API_KEY)

					try:
						nextGameId = rd.randint(0, min(10, len(matchlists["matches"])))
						print("random values for player: %d and match: %d" % (nextParticipantId, nextGameId))	
						matchId = matchlists["matches"][nextGameId]["gameId"]
						readable = True
					except KeyError:
						nextParticipantId = nextParticipantId % 10 + 1

				
			else:
				matchId = rd.randint(1796377995, 1796387995)
		df = pd.DataFrame(dataList)
		df.to_csv("data/match-list.csv", mode='a', header=False)
		dataList = []

#MatchCrawler(1796379999, API_KEY = "RGAPI-6b1ea488-6b90-467e-a4da-519d5a3aab2d",N = 100, M=10000)
