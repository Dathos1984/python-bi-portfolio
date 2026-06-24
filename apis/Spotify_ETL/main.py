import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

CLIENT_ID = '96988e00d1fc406f89e7c5cf47658428'
CLIENT_SECRET = 'cd69915a51c149429b5b89ebcb5a4be6'
REDIRECT_URI = 'http://127.0.0.1:8080/callback'
scope = "user-read-recently-played user-read-currently-playing"

if __name__ == "__main__":
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope
    ))
    recently_played = sp.current_user_recently_played(limit=5)
    file_json = "./apis/Spotify_ETL/mis_canciones_recientes.json"
    
    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(recently_played, file, indent=4, ensure_ascii=False)

    #print (json.dumps(recently_played, indent=4,ensure_ascii=False))

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in recently_played['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])
    
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }
    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    
    print(song_df)

    currently_playing = sp.current_user_playing_track()
    
    song_dict = {
        "song_name": [currently_playing['item']['name']],
        "artist_name": [currently_playing['item']['album']['artists'][0]['name']],
        "played_at": [currently_playing['item']['album']['release_date']],
        "timestamp": [currently_playing['item']['album']['release_date'][0:10]]
    }
    song_currently_playing_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    
    print(song_currently_playing_df)