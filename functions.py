from typing import Dict

from spotipy.oauth2 import SpotifyOAuth
import yaml


def get_params(params_file):
    with open(params_file, "r") as f:
        return yaml.safe_load(f)


def log_in(params: Dict[str, str]):
    return SpotifyOAuth(
        client_id=params["client_id"],
        client_secret=params["client_secret"],
        redirect_uri=params["redirect_uri"],
        scope="playlist-modify-private",
    )
