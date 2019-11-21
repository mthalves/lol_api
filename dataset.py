import requests
import pandas as pd

def __FetchAPI(URL, PARAMS = {}):
	try:
		return requests.get(url=URL, params=PARAMS).json()
	except:
		print("Bad request")

def __FetchMatch(matchId, API_KEY):
	URL = "https://br1.api.riotgames.com/lol/match/v4/matches/" + str(matchId)
	PARAMS = {'api_key': API_KEY}

	return __FetchAPI(URL, PARAMS)

def __ChampionIdHash():
	URL = "http://ddragon.leagueoflegends.com/cdn/9.23.1/data/en_US/champion.json"
	champData = __FetchAPI(URL)
	champData = champData["data"]
	champHash = {}
	
	for champion in champData:
		champHash[int(champData[champion]["key"])] = champion 

	return champHash

def ChampId2Name(id, champHash):
	if id < 0:
		return None
	else:
		return champHash[id]

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
				"champ2": ChampId2Name(data["participants"][1]["championId"], champHash),
				"lane2": data["participants"][1]["timeline"]["lane"],
				"champ3": ChampId2Name(data["participants"][2]["championId"], champHash),
				"lane3": data["participants"][2]["timeline"]["lane"],
				"champ4": ChampId2Name(data["participants"][3]["championId"], champHash),
				"lane4": data["participants"][3]["timeline"]["lane"],
				"champ5": ChampId2Name(data["participants"][4]["championId"], champHash),
				"lane5": data["participants"][4]["timeline"]["lane"],
				"champ6": ChampId2Name(data["participants"][5]["championId"], champHash),
				"lane6": data["participants"][5]["timeline"]["lane"],
				"champ7": ChampId2Name(data["participants"][6]["championId"], champHash),
				"lane7": data["participants"][6]["timeline"]["lane"],
				"champ8": ChampId2Name(data["participants"][7]["championId"], champHash),
				"lane8": data["participants"][7]["timeline"]["lane"],
				"champ9": ChampId2Name(data["participants"][8]["championId"], champHash),
				"lane9": data["participants"][8]["timeline"]["lane"],
				"champ10": ChampId2Name(data["participants"][9]["championId"], champHash),
				"lane10": data["participants"][9]["timeline"]["lane"],
				"team1win": game_result}
		return row

	except KeyError:
		print("Error: " + str(data["status"]["status_code"]) + ". Reason: " + data["status"]["message"])
	except :
		print("Wrong json format")

def MatchCrawler(initialId, API_KEY, N):
	print("Retriving Champion ID data...")
	champDict = __ChampionIdHash()
	dataList = []
	print("Retriving matches data:")
	for id in range(initialId, initialId+N):
		print("Retriving id: %d" % id)
		row = FetchMatchData(id, API_KEY, champDict)
		if row != None:
			dataList.append(row)

	df = pd.DataFrame(dataList)
	df.to_csv("data/match-list.csv", mode='a')

MatchCrawler(1796367986, API_KEY = "RGAPI-40995a70-ca55-4385-9711-3b12ff276de6",N = 10000)
