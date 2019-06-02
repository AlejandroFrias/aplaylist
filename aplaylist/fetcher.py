import time
import requests
from django.contrib.auth.models import User
from dict_digger import dig
from django.conf import settings
from retryable import retry
from spotipy.oauth2 import SpotifyOAuth


class SpotifyFetcher:
    def __init__(self, user_id):
        user = User.objects.get(pk=user_id)
        self.integration = user.integration

    @retry()
    def fetch_data(self, url, path_to_data=None, path_to_next=None):
        """Fetch data from spotify api

        Args:
            url (str): url path spotify api
            path_to_data (list): list style path to the items of interest. Default is to return all
                data as a dict instead of accumulating a list of data dicts
            path_to_next (list): list style path to the next url for pagination support
        """
        token = self.integration.access_token
        data = []
        all_data_loaded = False
        if "?" in url:
            url += f"&access_token={token}"
        else:
            url += f"?access_token={token}"

        while not all_data_loaded:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 204:
                return None  # no content
            else:
                response_json = response.json()

            if path_to_data:
                data += dig(response_json, *path_to_data)

                next_url = dig(response_json, *path_to_next) if path_to_next else None
                if next_url:
                    url = next_url + f"&access_token={token}"
                    time.sleep(0.1)
                else:
                    all_data_loaded = True
            else:
                data = response_json
                all_data_loaded = True

        return data
