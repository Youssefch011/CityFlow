def crowd_label(level):
    if level >= 80: return "Overcrowded"
    if level >= 60: return "Busy"
    if level >= 40: return "Moderate"
    return "Calm"

def crowd_color(level):
    if level >= 80: return "red"
    if level >= 60: return "orange"
    if level >= 40: return "blue"
    return "green"

def recommend_alternatives(locations, selected_name, user_interests=None):
    selected = locations[locations["name"] == selected_name].iloc[0]
    selected_category = selected["category"]
    user_interests = user_interests or []
    alternatives = locations[locations["name"] != selected_name].copy()
    alternatives["ai_score"] = 0
    alternatives["ai_score"] += (100 - alternatives["crowd_level"]) * 0.45
    alternatives["ai_score"] += alternatives["category"].apply(lambda x: 25 if x == selected_category else 0)
    alternatives["ai_score"] += alternatives["category"].apply(lambda x: 20 if x in user_interests else 0)
    alternatives["ai_score"] = alternatives["ai_score"].round(1)
    return alternatives.sort_values("ai_score", ascending=False).head(3)

def sustainability_score(crowd_level, transport=True):
    score = 100
    if crowd_level >= 80: score -= 35
    elif crowd_level >= 60: score -= 20
    elif crowd_level >= 40: score -= 10
    if transport: score += 10
    return min(score, 100)
