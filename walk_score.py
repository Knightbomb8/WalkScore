from walkscore import WalkScoreAPI
import math

api_key = 'YOUR API KEY GOES HERE'

def gather_walk_score(address: str) -> int:
    walkscore_api = WalkScoreAPI(api_key = api_key)
    return 1

def get_distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)

if __name__ == "__main__":
    point_a = (34.024382, -118.396126)
    point_b = (34.023278, -118.398889)
    print(get_distance(point_a, point_b))
    address = "2109 Mary Way, Placentia Ca 92870"