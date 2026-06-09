# CityFlow Complete Updated MVP

## Run the app
```bash
pip install -r requirements.txt
streamlit run app.py
```

## New features included
- Multilingual interface: English, Spanish, Catalan, French
- Login and registration simulation
- User storage in `data/users.csv`
- Daily 11:00 crowd email notifier script
- Crowd report feature
- Impact points system
- Badges and levels
- Leaderboard
- Reward marketplace simulation
- Admin dashboard

## Daily email notification
The file `daily_notifier.py` is prepared for Gmail SMTP.

For a real Gmail test:
1. Create a Gmail App Password.
2. Set these environment variables:
   - CITYFLOW_EMAIL
   - CITYFLOW_EMAIL_PASSWORD
3. Run:
```bash
python daily_notifier.py
```

For automatic 11:00 emails:
- Use Windows Task Scheduler
- Or GitHub Actions
- Or a cloud cron job

This is an academic MVP simulation.
