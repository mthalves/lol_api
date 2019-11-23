
# USE THIS CLASS WHEN YOU WILL MAKE THE BD OF YOUR ONLINE USER;
from request import request


class match:

    def __init__(self, matchId):
        self.request = request()

        response = self.request.getMatch(matchId)
        self.gameId = response['gameId']
