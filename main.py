import requests
import spotipy
import os
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = "https://www.billboard.com/charts/hot-100"
URL_DESIRED = f"{URL}/{date}/"

SPOTIFY_CLIENT_ID = os.environ.get("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://example.com"
PLAYLIST_ENDPOINT = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
USERNAME = os.environ.get("USERNAME")


response = requests.get(url=URL_DESIRED)
webpage = response.text
soup = BeautifulSoup(markup=webpage, features="html.parser")
song_names_spans = soup.select("div ul li ul li h3")

song_names = [song_title.getText().strip() for song_title in song_names_spans]

# playlist_header = {
#     "playlist_id": PLAYLIST_ID
# }
# playlist_data = {
#     "uris": song_names,
#     "position": 0
# }
# spotify_response = requests.post(url=PLAYLIST_ENDPOINT, params=playlist_data, headers=playlist_header)

#  First create the OAuth
access_token = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            show_dialog=True, cache_path="token.txt", scope="playlist-modify-private",
                            username=USERNAME)
#  We can create the playlist.
sp = spotipy.Spotify(auth_manager=access_token)

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    search_result = sp.search(q=f"{song} year:{year}", type="track")
    # pprint(search_result)
    try:
        uri = search_result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#  Creating new private playlist.
playlist_name = f"{date} Billboard 100"
playlist_description = "Billboard Hot 100 songs"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description, public=False)
#  Adding songs to the playlist.
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)




