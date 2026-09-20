# SignUpGenius sign-up sheet URLs to track. Add the public URLs you want
# scraped, e.g. "https://www.signupgenius.com/go/XXXXXXXXXXXX"
SIGNUP_GENIUS_URLS: list[str] = [
    "https://www.signupgenius.com/go/4090A49AAA72FAB9-57667538-steam?useFullSite=true#/",
]

# How often (minutes) the background scheduler re-scrapes, if enabled in main.py.
REFRESH_INTERVAL_MINUTES = 30
