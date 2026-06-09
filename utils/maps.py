from urllib.parse import quote_plus


def place_maps_url(name, lat, lon):
    query = quote_plus(f"{name} {lat},{lon}")
    return f"https://www.google.com/maps/search/?api=1&query={query}"


def directions_maps_url(origin_name, origin_lat, origin_lon, stops):
    origin = quote_plus(f"{origin_name} {origin_lat},{origin_lon}")
    if not stops:
        return f"https://www.google.com/maps/dir/?api=1&origin={origin}"

    destination = stops[-1]
    destination_query = quote_plus(f"{destination['place']} {destination['lat']},{destination['lon']}")
    waypoints = [
        quote_plus(f"{stop['place']} {stop['lat']},{stop['lon']}")
        for stop in stops[:-1]
    ]
    url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin}"
        f"&destination={destination_query}"
        "&travelmode=walking"
    )
    if waypoints:
        url += "&waypoints=" + "%7C".join(waypoints)
    return url
