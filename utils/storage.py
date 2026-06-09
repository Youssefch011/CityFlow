import csv
import os
from datetime import datetime

import pandas as pd

from utils.rewards import badge_from_points


USERS_FILE = "data/users.csv"
REPORTS_FILE = "data/reports.csv"
PREFERENCES_FILE = "data/preferences.csv"
ITINERARIES_FILE = "data/itineraries.csv"
REDEMPTIONS_FILE = "data/redemptions.csv"
LOCATIONS_FILE = "data/locations.csv"

USER_FIELDS = ["name", "email", "phone", "language", "points", "badge", "daily_alerts", "last_alert_sent"]
REPORT_FIELDS = ["name", "email", "location", "crowd_level", "comment", "photo_path", "points_awarded", "created_at"]
PREFERENCE_FIELDS = ["email", "interests", "travel_style", "updated_at"]
ITINERARY_FIELDS = ["email", "time", "place", "activity", "crowd_level", "area", "points_awarded", "created_at"]
REDEMPTION_FIELDS = ["email", "reward", "cost", "status", "created_at"]


def ensure_csv(file_path, fieldnames):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        return

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_fields = reader.fieldnames or []
        rows = list(reader)

    if existing_fields != fieldnames:
        migrated_rows = []
        for row in rows:
            migrated_rows.append({field: row.get(field, "") for field in fieldnames})
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(migrated_rows)


def ensure_data_files():
    ensure_csv(USERS_FILE, USER_FIELDS)
    ensure_csv(REPORTS_FILE, REPORT_FIELDS)
    ensure_csv(PREFERENCES_FILE, PREFERENCE_FIELDS)
    ensure_csv(ITINERARIES_FILE, ITINERARY_FIELDS)
    ensure_csv(REDEMPTIONS_FILE, REDEMPTION_FIELDS)


def read_csv(file_path, fieldnames):
    ensure_csv(file_path, fieldnames)
    return pd.read_csv(file_path)


def _read_dicts(file_path, fieldnames):
    ensure_csv(file_path, fieldnames)
    with open(file_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_dicts(file_path, fieldnames, rows):
    ensure_csv(file_path, fieldnames)
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_user_by_email(email):
    email = str(email or "").strip().lower()
    if not email:
        return None

    for row in _read_dicts(USERS_FILE, USER_FIELDS):
        if str(row.get("email", "")).strip().lower() == email:
            row["points"] = int(float(row.get("points") or 0))
            row["badge"] = badge_from_points(row["points"])
            return row
    return None


def save_user(name, email, phone, language, points=0, daily_alerts=True):
    email = str(email or "").strip()
    if not email:
        return None

    rows = _read_dicts(USERS_FILE, USER_FIELDS)
    existing = None
    for row in rows:
        if str(row.get("email", "")).strip().lower() == email.lower():
            existing = row
            break

    if existing:
        existing["name"] = name or existing.get("name") or "City Explorer"
        existing["phone"] = phone or existing.get("phone", "")
        existing["language"] = language or existing.get("language", "English")
        existing["points"] = str(int(float(existing.get("points") or points or 0)))
        existing["badge"] = badge_from_points(int(existing["points"]))
        if not existing.get("daily_alerts"):
            existing["daily_alerts"] = "yes" if daily_alerts else "no"
        else:
            existing["daily_alerts"] = "yes" if daily_alerts else "no"
        existing["last_alert_sent"] = existing.get("last_alert_sent", "")
    else:
        rows.append({
            "name": name or "City Explorer",
            "email": email,
            "phone": phone or "",
            "language": language or "English",
            "points": str(int(points or 0)),
            "badge": badge_from_points(int(points or 0)),
            "daily_alerts": "yes" if daily_alerts else "no",
            "last_alert_sent": "",
        })

    _write_dicts(USERS_FILE, USER_FIELDS, rows)
    return get_user_by_email(email)


def update_user_points(email, points):
    email = str(email or "").strip()
    if not email:
        return

    rows = _read_dicts(USERS_FILE, USER_FIELDS)
    updated = False
    for row in rows:
        if str(row.get("email", "")).strip().lower() == email.lower():
            row["points"] = str(int(points or 0))
            row["badge"] = badge_from_points(int(points or 0))
            updated = True
            break

    if updated:
        _write_dicts(USERS_FILE, USER_FIELDS, rows)


def get_daily_alert_users():
    users = []
    for row in _read_dicts(USERS_FILE, USER_FIELDS):
        email = str(row.get("email", "")).strip()
        wants_alerts = str(row.get("daily_alerts", "yes")).strip().lower() != "no"
        if email and wants_alerts:
            users.append(row)
    return users


def mark_alert_sent(email):
    email = str(email or "").strip().lower()
    if not email:
        return

    rows = _read_dicts(USERS_FILE, USER_FIELDS)
    for row in rows:
        if str(row.get("email", "")).strip().lower() == email:
            row["last_alert_sent"] = datetime.now().isoformat(timespec="seconds")
            break
    _write_dicts(USERS_FILE, USER_FIELDS, rows)


def save_preferences(email, interests, travel_style):
    email = str(email or "").strip()
    if not email:
        return

    rows = _read_dicts(PREFERENCES_FILE, PREFERENCE_FIELDS)
    payload = {
        "email": email,
        "interests": "|".join(interests or []),
        "travel_style": travel_style or "Balanced",
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    rows = [row for row in rows if str(row.get("email", "")).strip().lower() != email.lower()]
    rows.append(payload)
    _write_dicts(PREFERENCES_FILE, PREFERENCE_FIELDS, rows)


def get_preferences(email):
    email = str(email or "").strip().lower()
    if not email:
        return {"interests": [], "travel_style": "Balanced"}

    for row in reversed(_read_dicts(PREFERENCES_FILE, PREFERENCE_FIELDS)):
        if str(row.get("email", "")).strip().lower() == email:
            interests = [item for item in str(row.get("interests", "")).split("|") if item]
            return {"interests": interests, "travel_style": row.get("travel_style") or "Balanced"}
    return {"interests": [], "travel_style": "Balanced"}


def crowd_level_to_number(label):
    mapping = {
        "Calm": 30,
        "Moderate": 50,
        "Busy": 70,
        "Very Crowded": 90,
        "Overcrowded": 90,
    }
    return mapping.get(str(label), 50)


def save_report(name, email, location, crowd_level, comment, points_awarded, photo_path=""):
    ensure_csv(REPORTS_FILE, REPORT_FIELDS)
    with open(REPORTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REPORT_FIELDS)
        writer.writerow({
            "name": name or "City Explorer",
            "email": email or "",
            "location": location,
            "crowd_level": crowd_level,
            "comment": comment or "",
            "photo_path": photo_path or "",
            "points_awarded": int(points_awarded or 0),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        })


def delete_report_at_index(report_index):
    rows = _read_dicts(REPORTS_FILE, REPORT_FIELDS)
    try:
        index = int(report_index)
    except (TypeError, ValueError):
        return False

    if index < 0 or index >= len(rows):
        return False

    rows.pop(index)
    _write_dicts(REPORTS_FILE, REPORT_FIELDS, rows)
    return True


def update_location_crowd(location_name, observed_level):
    if not os.path.exists(LOCATIONS_FILE):
        return

    locations = pd.read_csv(LOCATIONS_FILE)
    observed = crowd_level_to_number(observed_level)
    mask = locations["name"] == location_name
    if mask.any():
        current = int(locations.loc[mask, "crowd_level"].iloc[0])
        locations.loc[mask, "crowd_level"] = round((current * 0.65) + (observed * 0.35))
        locations.to_csv(LOCATIONS_FILE, index=False, encoding="utf-8")


def save_itinerary(email, itinerary, points_by_place):
    ensure_csv(ITINERARIES_FILE, ITINERARY_FIELDS)
    created_at = datetime.now().isoformat(timespec="seconds")
    with open(ITINERARIES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ITINERARY_FIELDS)
        for item in itinerary:
            place = item.get("place", "")
            writer.writerow({
                "email": email or "",
                "time": item.get("time", ""),
                "place": place,
                "activity": item.get("activity", ""),
                "crowd_level": item.get("crowd_level", 0),
                "area": item.get("area", ""),
                "points_awarded": points_by_place.get(place, 0),
                "created_at": created_at,
            })


def save_redemption(email, reward, cost, status):
    ensure_csv(REDEMPTIONS_FILE, REDEMPTION_FIELDS)
    with open(REDEMPTIONS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REDEMPTION_FIELDS)
        writer.writerow({
            "email": email or "",
            "reward": reward,
            "cost": int(cost or 0),
            "status": status,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        })
