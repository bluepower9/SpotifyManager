from resources.SpotifyManager import SpotifyManager
import resources.generateplaylist as gp
import spotipy as spotify

def create_playlist(sp:SpotifyManager, songtype, name, public = True, description = ""):
    print("trying to generate", songtype, "playlist...")
    songs = gp.get_tracks_ml(sp, songtype, limit = 50)
    data = sp.create_playlist(name, public=public, description=description)
    sp.add_songs_to_playlist(data['id'], songs)
    print('successfully created playlist.')


if __name__ == '__main__':
    sp = SpotifyManager('bluepower9')
    tracks = sp.get_all_tracks()

    features = sp.get_features(tracks)
    sp.add_feature_data(features)

    trackdata = sp.get_track_data(tracks)
    sp.add_track_data(trackdata)

    albums = sp.get_albums()
    sp.add_album_data(albums)
    #print(sp.get_albums_genres())
    create_playlist(sp, 'feels', 'feels 1', public=False, description = "test of creating playlist")
    