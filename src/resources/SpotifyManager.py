import spotipy as spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json

CLIENT_ID = 'f08ae07406604a40bcefe35afeede42e'
CLIENT_SECRET = 'efc935fc9b9044f381a80b64450a7557'
scope = 'user-library-read playlist-modify-private playlist-modify-public'


class SpotifyManager:
    def __init__(self, username):
        self.client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.auth_manager = SpotifyOAuth(username=username,scope=scope, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = 'http://localhost:8888/callback', show_dialog=True)
        self.sp = spotify.Spotify(client_credentials_manager=self.client_credentials_manager, auth_manager=self.auth_manager)
        self.token = spotify.util.prompt_for_user_token(username, scope=scope, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = 'http://localhost:8888/callback', show_dialog=True)
        self.albums = {}
        self.trackfeatures = {}
        self.trackdata = {}

    
    def setup(self):
        tracks = self.get_all_tracks()

        features = self.get_features(tracks)
        self.add_feature_data(features)

        trackdata = self.get_track_data(tracks)
        self.add_track_data(trackdata)

        albums = self.get_albums()
        self.add_album_data(albums)


    def userid(self):
        return self.sp.current_user()['id']

    def get_username(self):
        return self.sp.current_user()['display_name']

    def get_playlist_tracks(self, playlist_id):
        '''
        takes in a playlist id
        returns a list of all the songs in that playlist.
        '''

        offset = 0
        tracks = []
        results = self.sp.playlist_tracks(playlist_id, limit = 100, offset = 0)
        
        while (len(results['items'])) > 0:
            for track in results['items']:
                try:
                    tracks.append(track['track']['href'].split('/')[-1])
                except TypeError as e:
                    print('failed to retrieve track')
            offset += 100
            results = self.sp.playlist_tracks(playlist_id, limit = 100, offset=offset)
    
        return tracks


    def get_all_tracks(self):
        offset = 0
        tracks = []
        results = self.sp.current_user_saved_tracks(limit=50, offset = 0)
        
        while len(results['items']) > 0:
            for track in results['items']:
                tracks.append(track['track']['href'].split('/')[-1])
            offset += 50
            results = self.sp.current_user_saved_tracks(limit=50, offset = offset)
        return tracks

    
    def get_albums_genres(self, albums=None):
        if albums is None:
            albums = self.albums.values()
        else:
            albums = [self.albums[album] for album in albums]
        
        result = {}
        for album in albums:
            result[album['id']] = album['genres']
        return result

    def get_track_data(self, tracks):
        size = 50
        if type(tracks) == str:
            return self.sp.track(tracks)
        result = []
        start = 0
        end = start + size
        if end > len(tracks):
            end = len(tracks)

        while start < len(tracks):
            features = self.sp.tracks(tracks= tracks[start:end])
            result += features['tracks']
            start += size
            end = start + size
            if end > len(tracks):
                end = len(tracks)
        
        return result

    
    def add_track_data(self, result):
        for track in result:
            self.trackdata[track['id']] = track



    def get_features(self, tracks:list) -> list:
        result = []
        start = 0
        end = start + 100
        if end > len(tracks):
            end = len(tracks)

        while start < len(tracks):
            features = self.sp.audio_features(tracks= tracks[start:end])
            result += features
            start += 100
            end = start + 100
            if end > len(tracks):
                end = len(tracks)
        
        return result


    def add_feature_data(self, result):
        for track in result:
            self.trackfeatures[track['id']] = track


    def get_albums(self, tracks = None):
        if tracks:
            trackdata = self.get_track_data(tracks)
        else:
            trackdata = self.trackdata.values()
        albums = list(set([track['album']['uri'].split(':')[-1] for track in trackdata]))

        limit = 20
        result = []
        start = 0
        end = start + limit
        if end > len(albums):
            end = len(albums)

        while start < len(albums):
            features = self.sp.albums(albums[start:end])
            result += features['albums']
            start += limit
            end = start + limit
            if end > len(albums):
                end = len(albums)
       
        return result


    def add_album_data(self, result):
        for album in result:
            self.albums[album['id']] = album


    def create_playlist(self, name, public = True, description = ""):
        print('trying to create playlist...')
        data = self.sp.user_playlist_create(self.userid(), name, public = public, description = description)
        print('successfully made playlist.')
        return data

    def add_songs_to_playlist(self, playlist_id, tracks, position=None):
        print('Trying to adding songs to playlist:', playlist_id)
        self.sp.user_playlist_add_tracks(self.userid(), playlist_id, tracks, position=position)
        print('Successsfully added songs to playlist.')


if __name__ == '__main__':
    sp = SpotifyManager('bluepower9')
    tracks = sp.get_all_tracks()
    features = sp.get_features(tracks)
    #print(features)
    #print(len(features))
    trackdata = sp.get_track_data(tracks)
    sp.add_track_data(trackdata)
    album_data = sp.get_albums()
    sp.add_album_data(album_data)
    
    #print(sp.get_albums_genres())
    #print(sp.get_playlist_tracks('37i9dQZF1DX4WYpdgoIcn6'))

    #with open('audio_analysis.txt' ,'w') as file:
    #    file.write(json.dumps(sp.sp.audio_analysis('1HimGOB6BjOaCQYMIF1xtU')))

    print(sp.sp.current_user())




