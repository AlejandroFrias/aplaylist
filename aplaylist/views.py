from aplaylist.fetcher import SpotifyFetcher
from django.shortcuts import render
import requests
import json


def home(request):
    return render(request, 'aplaylist/home.html')


def index(request):
    fetcher = SpotifyFetcher(request.user.id)
    token = fetcher.integration.access_token

    # currently playing data
    url = f"https://api.spotify.com/v1/me/player/currently-playing"
    raw_data = fetcher.fetch_data(url)
    if not raw_data:
        raw_data = "Nothing currently playing"

    # available devices data
    url = f"https://api.spotify.com/v1/me/player/devices?access_token={token}"
    devices_data = fetcher.fetch_data(url, ["devices"])

    context = {
        'albums': request.user.album_set.all(),
        'raw_data': json.dumps(raw_data),
        'devices_data': devices_data,
    }
    return render(request, 'aplaylist/index.html', context)

def play_album(request, spotify_id):
    fetcher = SpotifyFetcher(request.user.id)
    token = fetcher.integration.access_token
    url = f"https://api.spotify.com/v1/me/player/play?access_token={token}"
    return requests.put(url, json={"context_uri": f"spotify:album:{spotify_id}"})
