import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from html import escape

import pandas as pd

from utils.storage import get_daily_alert_users, mark_alert_sent


def _env(name, default=""):
    return os.environ.get(name, default).strip()


def _parse_time(value):
    try:
        return datetime.fromisoformat(str(value or ""))
    except ValueError:
        return None


def alert_due(user, now=None):
    now = now or datetime.now()
    last_sent = _parse_time(user.get("last_alert_sent", ""))
    return last_sent is None or now - last_sent >= timedelta(hours=24)


def _pressure_label(level):
    level = int(level)
    if level >= 80:
        return "Overcrowded"
    if level >= 60:
        return "Busy"
    if level >= 40:
        return "Moderate"
    return "Calm"


def _pressure_color(level):
    level = int(level)
    if level >= 80:
        return "#F43F5E"
    if level >= 60:
        return "#FB923C"
    if level >= 40:
        return "#38BDF8"
    return "#22C55E"


def _place_row(row):
    level = int(row["crowd_level"])
    return f"""
        <tr>
            <td style="padding:12px 0;border-bottom:1px solid rgba(226,232,240,.10);">
                <div style="font-weight:800;color:#FFFFFF;font-size:15px;line-height:1.2;">{escape(str(row['name']))}</div>
                <div style="color:#9FB6C8;font-size:12px;margin-top:4px;">{escape(str(row['area']))} · {escape(str(row['category']))}</div>
            </td>
            <td align="right" style="padding:12px 0;border-bottom:1px solid rgba(226,232,240,.10);">
                <span style="display:inline-block;min-width:78px;text-align:center;padding:7px 10px;border-radius:999px;background:{_pressure_color(level)};color:#FFFFFF;font-size:12px;font-weight:900;">{level}%</span>
                <div style="color:#9FB6C8;font-size:11px;margin-top:5px;">{escape(_pressure_label(level))}</div>
            </td>
        </tr>
    """


def build_daily_alert(user, locations):
    name = user.get("name") or "City Explorer"
    crowded = locations.sort_values("crowd_level", ascending=False).head(3)
    calm = locations.sort_values("crowd_level", ascending=True).head(3)
    top_hotspot = crowded.iloc[0]
    best_alternative = calm.iloc[0]
    avg_pressure = round(float(locations["crowd_level"].mean()), 1)
    crowded_count = int((locations["crowd_level"] >= 80).sum())
    calm_count = int((locations["crowd_level"] < 50).sum())
    pressure_drop = max(0, int(top_hotspot["crowd_level"]) - int(best_alternative["crowd_level"]))
    today = datetime.now().strftime("%A, %B %d")

    subject = f"CityFlow Daily Brief: {best_alternative['name']} is your calmer move today"
    crowded_lines = "\n".join(
        f"- {row['name']} ({int(row['crowd_level'])}% - {_pressure_label(row['crowd_level'])})"
        for _, row in crowded.iterrows()
    )
    calm_lines = "\n".join(
        f"- {row['name']} ({int(row['crowd_level'])}% - {_pressure_label(row['crowd_level'])})"
        for _, row in calm.iterrows()
    )
    text = f"""CityFlow Daily Brief
{today}

Hello {name},

Your calmer move today is {best_alternative['name']} in {best_alternative['area']}.
It is {pressure_drop}% calmer than {top_hotspot['name']} based on the current CityFlow prototype data.

City status:
- Average pressure: {avg_pressure}%
- Crowded zones: {crowded_count}
- Calm alternatives: {calm_count}

Avoid first:
{crowded_lines}

Better move:
Try {best_alternative['name']} in {best_alternative['area']}. It is currently tracking at {int(best_alternative['crowd_level'])}% crowd pressure and gives you a calmer city experience.

Calmer alternatives:
{calm_lines}

Why this matters:
Choosing lower-pressure places improves your visit and helps Barcelona distribute movement more fairly.
"""
    crowded_rows = "".join(_place_row(row) for _, row in crowded.iterrows())
    calm_rows = "".join(_place_row(row) for _, row in calm.iterrows())
    safe_name = escape(str(name))
    safe_best = escape(str(best_alternative["name"]))
    safe_best_area = escape(str(best_alternative["area"]))
    safe_hotspot = escape(str(top_hotspot["name"]))
    safe_today = escape(today)
    best_level = int(best_alternative["crowd_level"])
    best_label = escape(_pressure_label(best_level))

    html = f"""
    <div style="margin:0;padding:0;background:#03120D;">
        <div style="display:none;max-height:0;overflow:hidden;color:transparent;">Your CityFlow crowd brief: avoid pressure, choose the calmer move, and help Barcelona breathe.</div>
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:linear-gradient(135deg,#03120D 0%,#064E3B 45%,#082F49 100%);padding:28px 12px;font-family:Inter,Arial,sans-serif;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:680px;background:#071426;border:1px solid rgba(187,247,208,.22);border-radius:18px;overflow:hidden;box-shadow:0 28px 70px rgba(0,0,0,.34);">
                        <tr>
                            <td style="padding:26px;background:linear-gradient(135deg,#064E3B 0%,#0EA5E9 100%);">
                                <div style="display:inline-block;padding:7px 10px;border-radius:999px;background:rgba(2,8,23,.32);color:#D9F7FF;font-size:11px;font-weight:900;letter-spacing:.7px;text-transform:uppercase;">CityFlow Daily Brief · {safe_today}</div>
                                <h1 style="margin:14px 0 0;color:#FFFFFF;font-size:30px;line-height:1.08;font-weight:900;">Hello {safe_name}, choose the calmer move today.</h1>
                                <p style="margin:12px 0 0;color:#E6FFFA;font-size:15px;line-height:1.5;">Avoid <b>{safe_hotspot}</b> and try <b>{safe_best}</b> in <b>{safe_best_area}</b>. This choice is <b>{pressure_drop}% calmer</b> based on current CityFlow data.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:22px 26px 4px;">
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                    <tr>
                                        <td style="padding:10px;background:rgba(255,255,255,.055);border:1px solid rgba(103,232,249,.14);border-radius:12px;">
                                            <div style="color:#67E8F9;font-size:24px;font-weight:900;">{avg_pressure}%</div>
                                            <div style="color:#9FB6C8;font-size:11px;font-weight:800;text-transform:uppercase;">Average pressure</div>
                                        </td>
                                        <td width="10"></td>
                                        <td style="padding:10px;background:rgba(255,255,255,.055);border:1px solid rgba(103,232,249,.14);border-radius:12px;">
                                            <div style="color:#FCA5A5;font-size:24px;font-weight:900;">{crowded_count}</div>
                                            <div style="color:#9FB6C8;font-size:11px;font-weight:800;text-transform:uppercase;">Crowded zones</div>
                                        </td>
                                        <td width="10"></td>
                                        <td style="padding:10px;background:rgba(255,255,255,.055);border:1px solid rgba(103,232,249,.14);border-radius:12px;">
                                            <div style="color:#86EFAC;font-size:24px;font-weight:900;">{calm_count}</div>
                                            <div style="color:#9FB6C8;font-size:11px;font-weight:800;text-transform:uppercase;">Calm options</div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:18px 26px 0;">
                                <div style="padding:18px;border-radius:14px;background:linear-gradient(135deg,rgba(34,197,94,.14),rgba(14,165,233,.10));border:1px solid rgba(187,247,208,.20);">
                                    <div style="color:#BBF7D0;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.5px;">Recommended move</div>
                                    <div style="margin-top:6px;color:#FFFFFF;font-size:22px;font-weight:900;">{safe_best}</div>
                                    <div style="margin-top:6px;color:#D9F7FF;font-size:14px;line-height:1.45;">{safe_best_area} · {best_level}% crowd pressure · {best_label}</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:20px 26px 0;">
                                <h2 style="margin:0 0 8px;color:#FFFFFF;font-size:18px;">Avoid first</h2>
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0">{crowded_rows}</table>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:20px 26px 0;">
                                <h2 style="margin:0 0 8px;color:#FFFFFF;font-size:18px;">Calmer alternatives</h2>
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0">{calm_rows}</table>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:22px 26px 26px;">
                                <div style="padding:15px;border-radius:14px;background:rgba(2,8,23,.55);border:1px solid rgba(103,232,249,.18);color:#CFFAFE;font-size:13px;line-height:1.5;">
                                    <b style="color:#FFFFFF;">CityFlow impact:</b> choosing lower-pressure places improves your visit, supports calmer neighborhoods, and helps Barcelona distribute movement more fairly.
                                </div>
                                <div style="margin-top:18px;color:#7FA4B8;font-size:11px;line-height:1.45;text-align:center;">
                                    CityFlow prototype alert · Data from local CSV crowd model and community reports.
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </div>
    """
    return subject, text, html


def smtp_ready():
    return bool(_env("CITYFLOW_SMTP_HOST") and _env("CITYFLOW_SMTP_USER") and _env("CITYFLOW_SMTP_PASSWORD"))


def send_email(to_email, subject, text, html):
    host = _env("CITYFLOW_SMTP_HOST")
    port = int(_env("CITYFLOW_SMTP_PORT", "587"))
    username = _env("CITYFLOW_SMTP_USER")
    password = _env("CITYFLOW_SMTP_PASSWORD")
    sender = _env("CITYFLOW_EMAIL_FROM", username)

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(host, port, timeout=20) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)


def run_daily_alerts(dry_run=False):
    locations = pd.read_csv("data/locations.csv")
    users = [user for user in get_daily_alert_users() if alert_due(user)]
    sent = []
    skipped = []

    if not smtp_ready() and not dry_run:
        return {
            "sent": sent,
            "skipped": [user.get("email", "") for user in users],
            "error": "SMTP is not configured. Set CITYFLOW_SMTP_HOST, CITYFLOW_SMTP_USER, and CITYFLOW_SMTP_PASSWORD.",
        }

    for user in users:
        email = user.get("email", "").strip()
        if not email:
            continue
        subject, text, html = build_daily_alert(user, locations)
        if dry_run:
            skipped.append(email)
            continue
        send_email(email, subject, text, html)
        mark_alert_sent(email)
        sent.append(email)

    return {"sent": sent, "skipped": skipped, "error": ""}
