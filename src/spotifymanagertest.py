import resources.generateplaylist as gp
from resources.createplaylist import create_playlist
from resources.SpotifyManager import SpotifyManager

sp = SpotifyManager('user')
tracks = sp.get_all_tracks()

features = sp.get_features(tracks)
sp.add_feature_data(features)

trackdata = sp.get_track_data(tracks)
sp.add_track_data(trackdata)

albums = sp.get_albums()
sp.add_album_data(albums)

create_playlist(sp, 'feels', 'feels test', public=False, description = "test of a feels playlist")
create_playlist(sp, 'upbeat', 'upbeat test', public=False, description = "test of an upbeat playlist")
create_playlist(sp, 'chill', 'chill test', public=False, description = "test of a chill playlist")
create_playlist(sp, 'acoustic', 'acoustic test', public=False, description = "test of an acoustic playlist")

input('\nFinished creating playlists. Click Enter to exit.')