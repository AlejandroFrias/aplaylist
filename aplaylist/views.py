from aplaylist.fetcher import SpotifyFetcher
from django.shortcuts import render
import requests
import json


def home(request):
    return render(request, "aplaylist/home.html")


def index(request):
    fetcher = SpotifyFetcher(request.user.id)

    # currently playing data
    url = f"https://api.spotify.com/v1/me/player/currently-playing"
    current_play_data = fetcher.fetch_data(url)
    if not current_play_data:
        current_play_data = "Nothing currently playing"

    # available devices data
    url = f"https://api.spotify.com/v1/me/player/devices"
    devices_data = fetcher.fetch_data(url, ["devices"])
    device_id = None
    for device in devices_data:
        if device['is_active']:
            device_id = device['id']
        elif device_id is None:
            device_id = device['id']

    context = {
        "album_playlists": request.user.albumplaylist_set.all(),
        "current_play_data": json.dumps(current_play_data),
        "devices_data": devices_data,
        "device_id": device_id,
    }
    return render(request, "aplaylist/index.html", context)


def play_album(request, spotify_id, device_id):
    fetcher = SpotifyFetcher(request.user.id)
    token = fetcher.integration.access_token
    url = f"https://api.spotify.com/v1/me/player/play?access_token={token}&device_id={device_id}"
    return requests.put(url, json={"context_uri": f"spotify:album:{spotify_id}"})


def play_album_playlist(request, name, device_id):
    fetcher = SpotifyFetcher(request.user.id)
    token = fetcher.integration.access_token
    ap = request.user.albumplaylist_set.get(name=name)
    track_uris = []
    for album in ap.album_set.all():
        tracks_url = f"https://api.spotify.com/v1/albums/{album.spotify_id}/tracks"
        tracks_data = fetcher.fetch_data(tracks_url, ["items"], ["next"])
        track_uris.extend([td['uri'] for td in tracks_data])
    url = f"https://api.spotify.com/v1/me/player/play?access_token={token}&device_id={device_id}"
    return requests.put(url, json={"uris": track_uris[2:]})
