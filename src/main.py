import os
import pylast

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
LAST_FM_USERNAME = os.environ.get("LAST_FM_USERNAME")
LAST_FM_PASSWORD = pylast.md5(os.environ.get("LAST_FM_PASSWORD"))

lastfm = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=LAST_FM_USERNAME,
    password_hash=LAST_FM_PASSWORD,
)

user = lastfm.get_user(LAST_FM_USERNAME)
top_tracks= user.get_top_tracks(pylast.PERIOD_6MONTHS, limit=100)

print("Your top played tracks of the last 6 months:")
for i, track in enumerate(top_tracks):
    print(f"{i + 1}. {track.item} – {track.weight} plays")
