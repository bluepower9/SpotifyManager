from resources.SpotifyManager import SpotifyManager
from models.SongMultiClassifierModel import SongMultiClassifierModel
from torch import Tensor, load

TYPE_SORT = {
                'upbeat': lambda x: x['valence'] + x['danceability'] + x['energy']*.75,
                'relaxing': lambda x: (1-x['valence']) + (1-x['danceability']) + (1-x['energy']),
                'chill': lambda x: (x['mode'] == 1, x['time_signature'] != 3, ((1-abs(.5-x['valence']))*1.5 + (1-abs(.4-x['danceability'])) + (1 - abs(.5-x['energy'])*1.5)  + (1 - abs(120-x['tempo'])/120) + x['acousticness']*.25)),
                'sad': lambda x: (1-x['valence'])*2 + (1-x['danceability']) + (1-x['energy'])
}



def get_tracks(sp: SpotifyManager, songtype: str, limit = 10):
    if songtype not in TYPE_SORT.keys():
        print('unknown songtype: ' + songtype)
        return

    trackfeatures = list(sp.trackfeatures.values())
    tracks = sorted(trackfeatures, key = TYPE_SORT[songtype], reverse = True)[:limit]
    for i, track in enumerate(tracks):
        print('{:<4} {:-<50}  time sig: {:2}  valence: {:5}  danceability: {:5}  energy: {:5}  acousticness: {:5}  mode: {:5}'.format(str(i)+'.', sp.trackdata[track['id']]['name'][:50], track['time_signature'], track['valence'], track['danceability'], track['energy'], track['acousticness'], 'major' if track['mode'] else 'minor'))
    return [track['id'] for track in tracks]


def parse_feautures(sp: SpotifyManager):
    result = {}
    for track in sp.trackfeatures.values():
        result[track['id']] = [track['acousticness'], track['danceability'], track['energy'], track['instrumentalness'], track['liveness'], track['loudness'], track['speechiness'], track['valence'], track['tempo']]
    return result



def get_tracks_ml(sp: SpotifyManager, songtype: str, limit = 10):
    songtypes = {'chill': 0, 'upbeat': 1, 'feels': 2, 'acoustic': 3}
    if songtype not in songtypes:
        print("uknown songtype: ", songtype)
        return
    model = SongMultiClassifierModel(9)
    model.load_state_dict(load('./models/weights/weights5'))

    trackfeatures = parse_feautures(sp)
    output = []
    for id, features in trackfeatures.items():
        X = Tensor(features)
        out = model(X)
        output.append(out.tolist()+[id])
    
    output.sort(key = lambda x: x[songtypes[songtype]], reverse = True)
    for i, track in enumerate(output[:limit]):
        print('{:<4} {:-<50} {:<5}'.format(str(i)+'.', sp.trackdata[track[-1]]['name'][:50], track[songtypes[songtype]]))
    
    return [track[-1] for track in output[:limit]]
    



if __name__ == '__main__':
    sp = SpotifyManager('bluepower9')
    tracks = sp.get_all_tracks()

    features = sp.get_features(tracks)
    sp.add_feature_data(features)

    trackdata = sp.get_track_data(tracks)
    sp.add_track_data(trackdata)

    albums = sp.get_albums()
    sp.add_album_data(albums)

    get_tracks_ml(sp, 'upbeat', limit = 50)
    