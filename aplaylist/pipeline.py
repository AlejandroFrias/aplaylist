from .fetcher import SpotifyFetcher
from .models import Integration
from .models import Album
import json
from django.db.models.query_utils import Q


def save_integration(backend, user, response, *args, **kwargs):
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    integration_user_id = response["id"]
    if Integration.objects.filter(user=user).exists():
        Integration.objects.filter(user=user).update(
            access_token=access_token,
            refresh_token=refresh_token,
            integration_user_id=integration_user_id,
        )
    else:
        Integration.objects.create(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            integration_user_id=integration_user_id,
        )


def save_albums(backend, user, response, *args, **kwargs):
    fetcher = SpotifyFetcher(user.id)
    url = f"https://api.spotify.com/v1/me/albums"

    album_ids = []
    for album_data in fetcher.fetch_data(url, ["items"], ["next"]):
        album_ids.append(album_data["album"]["id"])
        if Album.objects.filter(name=album_data["album"]["name"]).exists():
            album = Album.objects.get(name=album_data["album"]["name"])
        else:
            album = Album()
        album.spotify_id = album_data["album"]["id"]
        album.name = album_data["album"]["name"]
        album.total_tracks = album_data["album"]["total_tracks"]
        album.save()

    # Default album playlist
    if user.albumplaylist_set.filter(name="Saved Albums").exists():
        ap = user.albumplaylist_set.get(name="Saved Albums")
        ap.album_set.clear()
    else:
        ap = user.albumplaylist_set.create(name="Saved Albums")
    ap.album_set.add(*Album.objects.filter(spotify_id__in=album_ids))
