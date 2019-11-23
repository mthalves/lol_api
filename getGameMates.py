from request import request


class user:
    URL = "https://br1.api.riotgames.com/lol/"  # URL BASE
    PARAMS = {'api_key': 'RGAPI-2d230ebe-a5e9-4e49-ba01-da132a9198c1'}

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
        response = self.request.getMatchList(self.summoner['accountId'])
        self.MatchList = response['matches']

        # Mastery Information -> (TO DO) get just what you want
        response = self.request.getMastery(self.summoner['id'])
        self.mastery = response


def main():
    SummonerName = input("Entre com o Summoner Name: ")
    u = user(SummonerName)

    print(u.mastery)


if __name__ == "__main__":
    main()
