from resources import generateplaylist as gp
from resources.SpotifyManager import SpotifyManager

sp = SpotifyManager('bluepower9')
tracks = sp.get_all_tracks()

features = sp.get_features(tracks)
sp.add_feature_data(features)

trackdata = sp.get_track_data(tracks)
sp.add_track_data(trackdata)

albums = sp.get_albums()
sp.add_album_data(albums)

gp.get_tracks_ml(sp, 'upbeat', limit = 50)