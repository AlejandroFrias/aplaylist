from .fetcher import SpotifyFetcher
from .models import Integration
from .models import Album
import json
from django.db.models.query_utils import Q

def save_integration(backend, user, response, *args, **kwargs):
    access_token        = response['access_token']
    refresh_token       = response['refresh_token']
    integration_user_id = response['id']
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
    url = f"https://api.spotify.com/v1/me/albums?access_token={fetcher.integration.access_token}"

    album_data_items = fetcher.fetch_data(url, ["items"], ["next"])
    user.album_set.all().delete()
    albums_to_create = []
    for album_data in album_data_items:
        albums_to_create.append(Album(
            user=user,
            spotify_id=album_data['album']['id'],
            name=album_data['album']['name'],
            total_tracks=album_data['album']['total_tracks'],
        ))

    Album.objects.bulk_create(albums_to_create)
