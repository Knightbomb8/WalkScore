from walkscore import WalkScoreAPI, LocationScore

api_key = 'YOUR API KEY GOES HERE'


class WalkScore:
    def __init__(self):
        self.api_key = self.load_api_key()
        self.walkscore_api = WalkScoreAPI(api_key = self.api_key)

    def get_walk_score(self, latitude: int, longitude: int) -> LocationScore:
        result = self.walkscore_api.get_score(latitude = latitude, longitude = longitude)
        return result

    def load_api_key(self) -> str:
        with open('walk_score_api_key.txt') as key_file:
            return key_file.readline()