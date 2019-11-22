import requests as r


class user:
    URL = "https://br1.api.riotgames.com/lol/"  # URL BASE
    PARAMS = {'api_key': 'RGAPI-2d230ebe-a5e9-4e49-ba01-da132a9198c1'}

    summoner = {}

    def __init__(self, SummonerName):
        full_URL = self.URL + "summoner/v4/summoners/by-name/"
        response = r.get(url=full_URL+SummonerName,
                         params=self.PARAMS).json()

        self.summoner['id'] = response['id']
        self.summoner['accountId'] = response['accountId']
        self.summoner['name'] = SummonerName


def main():
    SummonerName = input("Entre com o Summoner Name: ")
    u = user(SummonerName)

    print(u.summoner)


main()
