from math import atan2, cos, radians, sin, sqrt


PEAK_HOURS = {11, 12, 13, 17, 18, 19}
QUIET_HOURS = {8, 9, 15, 16}


def distance_km(a, b):
    lat1, lon1 = radians(float(a["lat"])), radians(float(a["lon"]))
    lat2, lon2 = radians(float(b["lat"])), radians(float(b["lon"]))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * atan2(sqrt(h), sqrt(1 - h))


def format_time(minutes):
    hour = (minutes // 60) % 24
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def projected_crowd(base_crowd, hour):
    adjustment = 0
    if hour in PEAK_HOURS:
        adjustment += 8
    if hour in QUIET_HOURS:
        adjustment -= 9
    if hour >= 20:
        adjustment -= 6
    return max(8, min(98, int(round(base_crowd + adjustment))))


def crowd_label(crowd):
    if crowd >= 80:
        return "high pressure"
    if crowd >= 60:
        return "busy but manageable"
    if crowd >= 40:
        return "moderate"
    return "calm"


def best_time_window(base_crowd):
    if base_crowd >= 80:
        return "08:30-10:30 or after 19:30"
    if base_crowd >= 65:
        return "09:00-11:00 or 15:00-17:00"
    if base_crowd >= 45:
        return "Most of the day is manageable"
    return "Good low-pressure choice anytime"


def activity_for(row, focus):
    category = str(row["category"])
    if focus == "Avoid queues":
        return "Use this stop as a lower-wait alternative to the crowded core"
    if focus == "Local discovery":
        return "Explore local streets nearby and support smaller neighborhood activity"
    if focus == "Culture and architecture":
        return f"Visit the {category.lower()} highlight with time to notice design details"
    if focus == "Beach reset":
        return "Take a slow outdoor break and reduce pressure on packed central areas"
    if focus == "Family friendly":
        return "Keep the pace simple with open space and predictable timing"
    if category in ["Food"]:
        return "Take a short market pause and choose off-peak food options"
    if category in ["Park", "Beach", "Waterfront", "Viewpoint"]:
        return "Recharge outdoors while avoiding the densest visitor flows"
    return f"Explore the {category.lower()} experience with a crowd-aware pace"


def local_tip_for(row):
    category = str(row["category"])
    if category in ["Beach", "Waterfront"]:
        return "Arrive earlier or later, walk one beach further, and avoid the busiest restaurant strip."
    if category in ["Park", "Viewpoint"]:
        return "Use this as a decompression stop between denser areas."
    if category in ["Architecture", "Culture", "Historic", "Monument"]:
        return "Pair it with a nearby calm street instead of rushing straight to the next icon."
    if category == "Food":
        return "Use off-peak food times to avoid queues and support vendors more evenly."
    return "Keep the visit flexible and move on if crowd pressure rises."


def score_destination(row, start_row, interests, focus, avoid_overcrowded, start_hour):
    crowd = projected_crowd(int(row["crowd_level"]), start_hour)
    score = 120 - crowd
    category = row["category"]

    if category in interests:
        score += 30
    if focus == "Culture and architecture" and category in ["Architecture", "Culture", "Historic", "Monument"]:
        score += 24
    if focus == "Beach reset" and category in ["Beach", "Waterfront"]:
        score += 26
    if focus == "Local discovery" and crowd < 55:
        score += 26
    if focus == "Avoid queues" and crowd < 50:
        score += 32
    if focus == "Family friendly" and category in ["Park", "Beach", "Waterfront"]:
        score += 20
    if focus == "Iconic Barcelona" and category in ["Architecture", "Historic", "Monument", "Culture"]:
        score += 18
    if avoid_overcrowded and crowd >= 80:
        score -= 65

    distance_penalty = 7.0 if focus == "Avoid queues" else 5.4
    if focus in ["Local discovery", "Family friendly"]:
        distance_penalty = 6.2
    score -= distance_km(start_row, row) * distance_penalty
    return round(score, 2)


def find_alternatives(locations, avoided_row, route_places, limit=3):
    same_category = locations[
        (locations["category"] == avoided_row["category"])
        & (~locations["name"].isin(route_places))
        & (locations["name"] != avoided_row["name"])
    ].copy()
    if same_category.empty:
        same_category = locations[
            (~locations["name"].isin(route_places))
            & (locations["name"] != avoided_row["name"])
        ].copy()

    same_category["distance_from_hotspot"] = same_category.apply(
        lambda row: distance_km(avoided_row, row),
        axis=1,
    )
    return same_category.sort_values(
        ["crowd_level", "distance_from_hotspot"],
        ascending=[True, True],
    ).head(limit).to_dict("records")


def build_route_insights(start_row, itinerary, locations, transport):
    if not itinerary:
        return {}

    start_crowd = int(start_row["crowd_level"])
    avg_crowd = sum(item["projected_crowd"] for item in itinerary) / len(itinerary)
    total_travel = sum(item["travel_minutes"] for item in itinerary)
    total_distance = sum(item["distance_km"] for item in itinerary)
    pressure_reduction = max(0, round(start_crowd - avg_crowd, 1))
    calm_stops = sum(1 for item in itinerary if item["projected_crowd"] < 50)
    busiest = sorted(itinerary, key=lambda item: item["projected_crowd"], reverse=True)[0]
    avoided = locations[locations["crowd_level"] >= 80].sort_values("crowd_level", ascending=False).head(3)

    score = 50
    score += min(30, pressure_reduction * 1.2)
    score += calm_stops * 5
    score += 8 if transport else 0
    score -= max(0, total_travel - 90) * 0.08

    return {
        "avg_crowd": round(avg_crowd, 1),
        "start_crowd": start_crowd,
        "pressure_reduction": pressure_reduction,
        "total_travel": int(total_travel),
        "total_distance": round(total_distance, 1),
        "calm_stops": calm_stops,
        "busiest_stop": busiest["place"],
        "busiest_crowd": busiest["projected_crowd"],
        "impact_score": int(max(0, min(100, round(score)))),
        "avoided_hotspots": avoided["name"].tolist(),
        "summary": (
            f"This route lowers expected crowd exposure by about {pressure_reduction}% "
            f"compared with starting at {start_row['name']} and keeps {calm_stops} stops under 50% pressure."
        ),
        "smart_explanation": (
            f"CityFlow moved the route away from {start_row['name']} because it is tracking at "
            f"{start_crowd}% pressure, then balanced lower crowd exposure, distance, category match, "
            f"and practical walking/transit time."
        ),
    }


def generate_itinerary(
    locations,
    selected_name,
    interests=None,
    start_hour=10,
    duration_hours=4,
    pace="Balanced",
    focus="Smart balanced",
    avoid_overcrowded=True,
    transport=True,
):
    interests = interests or []
    start_row = locations[locations["name"] == selected_name].iloc[0]
    candidates = locations[locations["name"] != selected_name].copy()
    candidates["smart_score"] = candidates.apply(
        lambda row: score_destination(row, start_row, interests, focus, avoid_overcrowded, start_hour),
        axis=1,
    )

    stop_duration = {"Relaxed": 80, "Balanced": 60, "Fast": 45}.get(pace, 60)
    travel_buffer = {"Relaxed": 26, "Balanced": 20, "Fast": 15}.get(pace, 20)
    available_minutes = int(duration_hours * 60)
    max_stops = max(2, min(5, available_minutes // (stop_duration + travel_buffer)))

    route = []
    current = start_row
    remaining = candidates.to_dict("records")
    cluster_penalty = 7.5 if transport else 10.0
    while remaining and len(route) < max_stops:
        remaining.sort(
            key=lambda row: (
                row["smart_score"] - (distance_km(current, row) * cluster_penalty),
                -int(row["crowd_level"]),
            ),
            reverse=True,
        )
        next_stop = remaining.pop(0)
        route.append(next_stop)
        current = next_stop

    itinerary = []
    current_minutes = int(start_hour * 60)
    previous = start_row
    route_places = [row["name"] for row in route]
    for index, row in enumerate(route, start=1):
        travel_km = distance_km(previous, row)
        travel_minutes = max(8, round(travel_km * (7 if transport else 10)))
        if index == 1:
            travel_minutes = max(10, travel_minutes)
        arrival = current_minutes + travel_minutes
        leave = arrival + stop_duration
        arrival_hour = arrival // 60
        base_crowd = int(row["crowd_level"])
        expected_crowd = projected_crowd(base_crowd, arrival_hour)
        alternatives = find_alternatives(locations, row, route_places, limit=2)
        start_pressure_gap = int(start_row["crowd_level"]) - expected_crowd
        confidence = min(94, max(58, 72 + (10 if expected_crowd < 60 else 0) + (6 if row["category"] in interests else 0) - int(travel_km > 4) * 5))
        pressure_phrase = (
            f"{start_pressure_gap}% calmer than {start_row['name']}"
            if start_pressure_gap > 0
            else f"keeps the route close to {start_row['name']} while monitoring pressure"
        )

        itinerary.append({
            "time": f"{format_time(arrival)}-{format_time(leave)}",
            "place": row["name"],
            "activity": activity_for(row, focus),
            "crowd_level": base_crowd,
            "projected_crowd": expected_crowd,
            "area": row["area"],
            "category": row["category"],
            "description": row.get("description", ""),
            "lat": float(row["lat"]),
            "lon": float(row["lon"]),
            "smart_score": row["smart_score"],
            "travel_minutes": travel_minutes,
            "duration_minutes": stop_duration,
            "distance_km": round(travel_km, 1),
            "best_time": best_time_window(base_crowd),
            "crowd_label": crowd_label(expected_crowd),
            "local_tip": local_tip_for(row),
            "alternatives": alternatives,
            "confidence": confidence,
            "decision_note": (
                f"Selected because it is {pressure_phrase}, fits the {focus.lower()} goal, "
                f"and is about {round(travel_km, 1)} km from the previous stop."
            ),
            "reason": (
                f"{row['area']} is a {crowd_label(expected_crowd)} stop at this time. "
                f"It is {pressure_phrase} and keeps the route within a practical travel radius."
            ),
        })
        current_minutes = leave
        previous = row

    insights = build_route_insights(start_row, itinerary, locations, transport)
    return itinerary, insights
