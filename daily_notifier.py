import os, smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = os.getenv("CITYFLOW_EMAIL")
PASSWORD = os.getenv("CITYFLOW_EMAIL_PASSWORD")

def build_message():
    locations = pd.read_csv("data/locations.csv")
    crowded = locations[locations["crowd_level"] >= 80]
    calm = locations[locations["crowd_level"] < 50].head(3)

    crowded_lines = "\n".join([f"- {r['name']}: {r['crowd_level']}%" for _, r in crowded.iterrows()])
    calm_lines = "\n".join([f"- {r['name']} ({r['area']})" for _, r in calm.iterrows()])

    return f"""Good morning,

Here is your CityFlow daily crowd alert for Barcelona.

Highly crowded areas today:
{crowded_lines}

Recommended calmer alternatives:
{calm_lines}

Tip: choose a low-crowd itinerary today and earn impact points.

CityFlow Team
"""

def send_email(to_email, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = to_email
    msg["Subject"] = "CityFlow Daily Crowd Alert - 11:00"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg)

def main():
    if not SENDER or not PASSWORD:
        print("Missing CITYFLOW_EMAIL or CITYFLOW_EMAIL_PASSWORD environment variables.")
        return

    users = pd.read_csv("data/users.csv")
    body = build_message()

    for _, user in users.iterrows():
        email = str(user.get("email", "")).strip()
        if email and email != "nan":
            send_email(email, body)
            print(f"Sent to {email}")

if __name__ == "__main__":
    main()
