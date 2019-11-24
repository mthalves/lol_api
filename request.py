import requests as r

class request:

    URL = "https://br1.api.riotgames.com/lol/"  # URL BASE
    PARAMS = {'api_key': 'RGAPI-e288b45f-8343-4bf4-baf2-8814e3ac9624'}

    def getUser(self, SummonerName):
        full_URL = self.URL + "summoner/v4/summoners/by-name/"
        response = r.get(url=full_URL+SummonerName,
                         params=self.PARAMS).json()
        return response

    def getMatchList(self, accountId):
        full_URL = self.URL + "match/v4/matchlists/by-account/"
        response = r.get(url=full_URL+accountId,
                         params=self.PARAMS).json()

        return response

    def getMastery(self, encryptedSummonerId):
        full_URL = self.URL + "champion-mastery/v4/champion-masteries/by-summoner/"
        response = r.get(url=full_URL+encryptedSummonerId,
                         params=self.PARAMS).json()

        return response


'''
        return response
        full_URL = self.URL + "champion-mastery/v4/champion-masteries/by-summoner/"
        self.masteryChampions = r.get(url=full_URL+self.summoner['id'],
                                      params=self.PARAMS).json()
'''
