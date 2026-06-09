def calculate_points(crowd_level, transport=True):
    points = 10
    if crowd_level < 50:
        points += 35
    elif crowd_level < 70:
        points += 18
    if transport:
        points += 25
    return points

def report_points():
    return 20

def badge_from_points(points):
    if points >= 1000:
        return "Urban Hero"
    if points >= 600:
        return "CityFlow Ambassador"
    if points >= 300:
        return "Sustainable Traveler"
    if points >= 100:
        return "Local Supporter"
    return "Explorer"

def reward_marketplace():
    return [
        {"reward": "5% discount at local café", "cost": 100},
        {"reward": "Free museum audio guide", "cost": 250},
        {"reward": "Tourist pass discount", "cost": 500},
        {"reward": "Free attraction ticket draw", "cost": 1000},
    ]
