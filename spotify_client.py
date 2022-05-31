
import spotipy
import json
import webbrowser
import creds
import random
import time

username = 'lokidoki'
client_id = creds.client_id
client_secret = creds.client_secrect
redirect_uri = 'http://google.com/'
cache = '.spotipyoauthcache'
SCOPE = 'user-library-read'


oauth_obj = spotipy.SpotifyOAuth(client_id, client_secret, redirect_uri)
token_dict = oauth_obj.get_access_token()
token = token_dict['access_token']

spotify_obj = spotipy.Spotify(auth=token)


user = spotify_obj.current_user()
json.dumps(user)

 
def playsong(fang):
    # cnt = 0
    recommendation_dict = {
        "Angry":['top metal songs','metal mix','rage workout','beast  mode'],
        "Sad": ['english breakup songs','sad hindi songs'],
        "Neutral":['all time hit international songs','pop hits 2022','all time pop hits'],
        "Happy":['harry styles','elvis presely'],
        "Disgust":[],
        "Surprise":['alan walker','martin garix'],
        "Fear":[]

    }
    song_data = recommendation_dict[fang][random.randint(0,len(recommendation_dict[fang])-1)]
    search_res = spotify_obj.search(song_data, 4, 0, 'playlist')
    playlist_dict = search_res['playlists']
    
    # webbrowser.open(sample_playlist)

    # track_id, track_name = [], []
    while(1):
        sample_playlist = playlist_dict['items'][random.randint(0,3)]['uri']
        plst_id = sample_playlist.split(':')[2]
        plst = spotify_obj.user_playlist_tracks('spotify', plst_id)['items']
        ran_track = random.randint(0,len(plst)-1)
        track_id = plst[ran_track]['track']['id']
        track_name = plst[ran_track]['track']['id']
        sng_drtn = spotify_obj.audio_features(track_id)[0]['duration_ms']
        webbrowser.open(f'spotify:track:{track_id}')
        print(sng_drtn)
        time.sleep(sng_drtn/1000)


    # for track in plst:
    #     track_name.append(track['track']['name'])
    #     track_id.append(track['track']['id'])
    #     # print(track_id,track_name)

    # while(1):
    #     ran_song = random.randint(0,len(track_id))
    #     webbrowser.open(f'spotify:track:{track_id[ran_song]}')
    #     sng_drtn = spotify_obj.audio_features(track_id[ran_song])[0]['duration_ms']
    #     print(track_name,sng_drtn)
    #     time.sleep((sng_drtn/1000)-1)
        



        # webbrowser.open(f'spotify:track:{track_id[0]}')
# spotify_obj.add_to_queue(track_id[3])


# track_name[5], track_id[5], spotify_obj.audio_features(track_id[5])[
#     0]['duration_ms']

