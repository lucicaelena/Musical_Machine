from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year would you like to travel to? please enter in this format (YYYY-MM-DD): ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="7db58e9dc09d42d39474c3b4479961ba",
        client_secret="0efdeefd0c994b1eba657cd8060b4f36",
        show_dialog=True,
        cache_path="token.txt",
        username="Lucy",
    ))
user_id = sp.current_user()["id"]
year = date.split("-")[0]
song_uris = []

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)