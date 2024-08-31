import random

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '77cc1040fc6d45a2903f6b1b4a8cf0c1'
CLIENT_SECRET = 'c7c38927128d42a19f9133ffca2b3c24'


def get_recommendations_for_song(sp, song_name, limit=5):
    results = sp.search(q=song_name, type='track', limit=1)
    if len(results['tracks']['items']) == 0:
        print(f"No results found for '{song_name}'")
        return []

    song_id = results['tracks']['items'][0]['id']
    recommendations = sp.recommendations(seed_tracks=[song_id], limit=limit)

    return [(track['name'], track['artists'][0]['name']) for track in recommendations['tracks']]


def read_songs_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()].remove("\n")


def write_songs_to_file(filename, all_songs):
    with open(filename, 'w') as file:
        for song in all_songs:
            file.write(f"{song}\n")


def shuffle_and_append_recommendations(filename, recommendations):
    with open(filename, 'a') as file:
        for title, artist in recommendations:
            file.write(f"\n{title} by {artist}")

    all_songs = read_songs_from_file(filename)
    random.shuffle(all_songs)
    write_songs_to_file(filename, all_songs)


def main():
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    song_titles = read_songs_from_file('/Users/lielmachluf/IdeaProjects/playerTest/src/main/java//songs.txt')

    all_recommendations = []
    for song in song_titles:
        print(f"Getting recommendations for '{song}':")
        recommendations = get_recommendations_for_song(sp, song)
        all_recommendations.extend(recommendations)
        for title, artist in recommendations:
            print(f"  - {title} by {artist}")
        print()
    shuffle_and_append_recommendations('/Users/lielmachluf/IdeaProjects/playerTest/src/main/java//songs.txt', all_recommendations)


if __name__ == "__main__":
    main()
