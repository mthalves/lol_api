from request import request

import pandas as pd

class user:
    URL = "https://br1.api.riotgames.com/lol/"  # URL BASE
    PARAMS = {'api_key': 'RGAPI-e288b45f-8343-4bf4-baf2-8814e3ac9624'}

    summoner = {}
    MatchList = {}

    def __init__(self, SummonerName):
        self.request = request()

        # user information (online user)
        response = self.request.getUser(SummonerName)
        self.summoner['id'] = response['id']
        self.summoner['accountId'] = response['accountId']
        self.summoner['name'] = SummonerName

        # MatchList Information -> (TO DO) get just what you want
        # Getting just the games in Summoner's Rift
        response = self.request.getMatchList(self.summoner['accountId'])
        self.MatchList = pd.DataFrame(response['matches'])
        self.MatchList =  self.MatchList.loc[self.MatchList['queue'] == 420]
        
        # Getting just the right lanes and roles combinations
        
        # role = NONE and lane = Jungle indicates player went jungle
        # role = SOLO and lane = MID/TOP indicates player went MID or TOP
        # role = DUO_SUPPORT and lane = BOTTOM indicates player went support
        # role = DUO_CARRT and lane = BOTTOM indicates player went ADC

        # All the other combinations are not right for us

        self.MatchList =  self.MatchList.loc[((self.MatchList['role'] == 'NONE') & (self.MatchList['lane'] == 'JUNGLE'))
        |  ((self.MatchList['lane'] == 'MID') &(self.MatchList['role'] == 'SOLO'))
        |  ((self.MatchList['lane'] == 'TOP') &(self.MatchList['role'] == 'SOLO'))
        |  ((self.MatchList['lane'] == 'BOTTOM') &(self.MatchList['role'] == 'DUO_SUPPORT'))
        |  ((self.MatchList['lane'] == 'BOTTOM') &(self.MatchList['role'] == 'DUO_CARRY'))]

        # Mastery Information -> (TO DO) get just what you want
        response = self.request.getMastery(self.summoner['id'])
        self.mastery = response


def main():
    SummonerName = input("Entre com o Summoner Name: ")
    u = user(SummonerName)

    print(u.MatchList)


if __name__ == "__main__":
    main()