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


# connect to last.fm
lastfm = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
    username=LAST_FM_USERNAME,
    password_hash=LAST_FM_PASSWORD,
)

SCOPE = "user-library-read"
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(scope=SCOPE))

# get top tracks from last.fm
user = lastfm.get_user(LAST_FM_USERNAME)
top_tracks_raw = user.get_top_tracks(pylast.PERIOD_6MONTHS, limit=300)
top_tracks = {}


for track in top_tracks_raw:
    if track.weight < 5:
        break
    song = (track.item.title, track.item.artist.name)
    plays = track.weight
    top_tracks[song] = plays

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

played_tracks = {}
unplayed_tracks = set()
for item in playlist_tracks:
    track = item["track"]
    pair = (track["name"], track["album"]["artists"][0]["name"])
    if pair in top_tracks:
        played_tracks[pair] = top_tracks[pair]
    else:
        unplayed_tracks.add(pair)

print("Most played tracks in the playlist:")
for i, (pair, plays) in enumerate(
    sorted(played_tracks.items(), key=lambda item: item[1], reverse=True)
):
    print(f"{i}. {pair[1]} – {pair[0]} – {plays} plays")

print("\nMost skipped tracks (<5 plays each):")
for pair in unplayed_tracks:
    print(f"{pair[1]} – {pair[0]}")
