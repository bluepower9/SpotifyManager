import csv, os
from SpotifyManager import SpotifyManager
import pandas as pd
import json


def write_csv(filename, fieldnames, data: list):
    print('trying to create and write to file:', filename, '...')
    with open(filename, 'w', newline = '') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:   #item should be a dict with keys matching fieldnames
            writer.writerow(item)

    print('successfully wrote to file.')


def get_links(path):
    ids = []
    with open(path,'r') as f:
        ids += [id.split(':')[-1].strip() for id in f.readlines()]
    return ids

def remove_valid_from_invalid(valid, invalid):
    #removes invalid ids that are found in valid from invalid to prevent duplication.
    for id in valid:
        if id in invalid:
            invalid.remove(id)


def get_features(sp, ids):
    features = sp.get_features(ids)
    for track in features:
        track.pop('id')
        track.pop('duration_ms')
        track.pop('analysis_url')
        track.pop('track_href')
        track.pop('uri')
        track.pop('type')
        track.pop('key')
        track.pop('mode')
        track.pop('time_signature')
    return features


def get_data(sp: SpotifyManager, songtypes: dict):
    #valid_ids: ids of songs that pass as type of track (ex. chill songs vs not chill songs)
    #invalid_ids: ids of songs that aren't part of the type of song.
    with open('SongTypes.json') as file:
        types = json.load(file)
    
    result = []
    
    for songtype, playlists in songtypes.items():
        ids = []
        for playlist in playlists:
            ids += sp.get_playlist_tracks(playlist)
        ids = list(set(ids))
        features = get_features(sp, ids)
        for track in features:
            #sets value for songtype to 1
            track[songtype] = 1
            
            #sets values for other songtype results to 0
            for othersongtype in songtypes.keys():
                if othersongtype != songtype:
                    track[othersongtype] = 0
        result += features

    return result


if __name__ == '__main__':
    sp = SpotifyManager('bluepower9')
    songtypes = {}
    songtypes['chill'] = get_links('data/links/chill.txt')
    songtypes['upbeat'] = get_links('data/links/upbeat.txt')
    songtypes['feels'] = get_links('data/links/feels.txt')
    songtypes['acoustic'] = get_links('data/links/acoustic.txt')
    data = get_data(sp, songtypes)
    
    #last 4 are playlist types
    fieldnames = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo', 'chill', 'upbeat', 'feels', 'acoustic']
    write_csv('data.csv', fieldnames, data)
   
    #x = pd.read_csv('chill.csv')
    #x = [list(x[:-2]) for x in x.values]
    #print(x)