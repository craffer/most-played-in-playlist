import os
import pylast
import spotipy

LASTFM_API_KEY = os.environ.get("API_KEY")
LASTFM_API_SECRET = os.environ.get("API_SECRET")
LAST_FM_USERNAME = os.environ.get("LAST_FM_USERNAME")
LAST_FM_PASSWORD = pylast.md5(os.environ.get("LAST_FM_PASSWORD"))
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")
PLAYLIST_NAME = "the good stuff"


lastfm = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
    username=LAST_FM_USERNAME,
    password_hash=LAST_FM_PASSWORD,
)

SCOPE = "user-library-read"
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(scope=SCOPE))
user = lastfm.get_user(LAST_FM_USERNAME)
top_tracks = user.get_top_tracks(pylast.PERIOD_6MONTHS, limit=300)

print("Your top played tracks of the last 6 months:")
for i, track in enumerate(top_tracks):
    if track.weight < 5:
        break
user_playlists = sp.current_user_playlists()
selected_playlist = None
for playlist in user_playlists["items"]:
    if playlist["name"] == PLAYLIST_NAME:
        selected_playlist = playlist

if selected_playlist is not None:
    playlist_id = selected_playlist["id"]

playlist_tracks = []
current_result = sp.playlist_tracks(playlist_id, limit=100)
page_number = 0
while current_result:
    playlist_tracks.extend(current_result["items"])
    current_result = sp.next(current_result)
