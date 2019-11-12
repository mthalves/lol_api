import requests


def FetchMatch(matchId):
	URL = "https://br1.api.riotgames.com/lol/match/v4/matches/" + str(matchId)
	PARAMS = {'api_key': 'RGAPI-be8953ce-255b-4dd2-98d8-883c68823eb2'}

	return __FetchAPI(URL, PARAMS)

def FetchMatchData(matchId):
	data = FetchMatch(matchId)

	game 
	row = { "id": 	data["gameId"],
			"ban1": data["participantIdentities"]["teams"][0]["ban"][0]["championId"],
			"ban2": data["participantIdentities"]["teams"][0]["ban"][1]["championId"],
			"ban3": data["participantIdentities"]["teams"][0]["ban"][2]["championId"],
			"ban4": data["participantIdentities"]["teams"][0]["ban"][3]["championId"],
			"ban5": data["participantIdentities"]["teams"][0]["ban"][4]["championId"],
			"ban6": data["participantIdentities"]["teams"][1]["ban"][0]["championId"],
			"ban7": data["participantIdentities"]["teams"][1]["ban"][1]["championId"],
			"ban8": data["participantIdentities"]["teams"][1]["ban"][2]["championId"],
			"ban9": data["participantIdentities"]["teams"][1]["ban"][3]["championId"],
			"ban10": data["participantIdentities"]["teams"][1]["ban"][4]["championId"],
			"champ1": data["participantIdentities"]["participants"][0]["championId"],
			"lane1": data["participantIdentities"]["participants"][0]["timeline"]["lane"],
			"champ2": data["participantIdentities"]["participants"][1]["championId"],
			"lane2": data["participantIdentities"]["participants"][1]["timeline"]["lane"],
			"champ3": data["participantIdentities"]["participants"][2]["championId"],
			"lane3": data["participantIdentities"]["participants"][2]["timeline"]["lane"],
			"champ4": data["participantIdentities"]["participants"][3]["championId"],
			"lane4": data["participantIdentities"]["participants"][3]["timeline"]["lane"],
			"champ5": data["participantIdentities"]["participants"][4]["championId"],
			"lane5": data["participantIdentities"]["participants"][4]["timeline"]["lane"],
			"champ6": data["participantIdentities"]["participants"][5]["championId"],
			"lane6": data["participantIdentities"]["participants"][5]["timeline"]["lane"],
			"champ7": data["participantIdentities"]["participants"][6]["championId"],
			"lane7": data["participantIdentities"]["participants"][6]["timeline"]["lane"],
			"champ8": data["participantIdentities"]["participants"][7]["championId"],
			"lane8": data["participantIdentities"]["participants"][7]["timeline"]["lane"],
			"champ9": data["participantIdentities"]["participants"][8]["championId"],
			"lane9": data["participantIdentities"]["participants"][8]["timeline"]["lane"],
			"champ10": data["participantIdentities"]["participants"][9]["championId"],
			"lane10": data["participantIdentities"]["participants"][9]["timeline"]["lane"],
			"team1win": game_result}

print(FetchMatch(1787536317))