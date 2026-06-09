import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.email_alerts import build_daily_alert, send_email, smtp_ready, run_daily_alerts
from utils.storage import get_daily_alert_users
import pandas as pd


def preview_alert():
    users = get_daily_alert_users()
    if not users:
        print("No users subscribed to daily alerts.")
        return
    locations = pd.read_csv(ROOT / "data" / "locations.csv")
    subject, text, _ = build_daily_alert(users[0], locations)
    print(subject)
    print("-" * len(subject))
    print(text)


def send_test_alert(to_email):
    if not smtp_ready():
        print("ERROR: SMTP is not configured. Set CITYFLOW_SMTP_HOST, CITYFLOW_SMTP_USER, and CITYFLOW_SMTP_PASSWORD.")
        return

    users = get_daily_alert_users()
    user = next((item for item in users if item.get("email", "").lower() == to_email.lower()), None)
    if user is None:
        user = {"name": "City Explorer", "email": to_email}

    locations = pd.read_csv(ROOT / "data" / "locations.csv")
    subject, text, html = build_daily_alert(user, locations)
    send_email(to_email, subject, text, html)
    print(f"Sent test alert to {to_email}")


def main():
    parser = argparse.ArgumentParser(description="Send CityFlow daily crowd alert emails.")
    parser.add_argument("--dry-run", action="store_true", help="List due users without sending email.")
    parser.add_argument("--preview", action="store_true", help="Print a sample email for the first subscribed user.")
    parser.add_argument("--to", help="Send one test alert immediately to this email address.")
    args = parser.parse_args()

    if args.preview:
        preview_alert()
        return

    if args.to:
        send_test_alert(args.to)
        return

    result = run_daily_alerts(dry_run=args.dry_run)
    if result.get("error"):
        print(f"ERROR: {result['error']}")
    print(f"Sent: {len(result['sent'])}")
    print(f"Skipped: {len(result['skipped'])}")
    if result["sent"]:
        print("Sent to:", ", ".join(result["sent"]))
    if result["skipped"]:
        print("Skipped:", ", ".join(result["skipped"]))


if __name__ == "__main__":
    main()
