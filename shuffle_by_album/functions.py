import random
from typing import Dict, List

from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import yaml


def get_params(params_file: str) -> Dict[str, str]:
    """"""
    with open(params_file, "r") as f:
        return yaml.safe_load(f)


def log_in(params: Dict[str, str]) -> Spotify:
    """"""
    return SpotifyOAuth(
        client_id=params["client_id"],
        client_secret=params["client_secret"],
        redirect_uri=params["redirect_uri"],
        scope="playlist-modify-private",
    )


@st.cache
def playlist_id_dict(client: Spotify) -> Dict[str, str]:
    """"""
    playlists = client.current_user_playlists()["items"]
    return {p["name"]: p["id"] for p in playlists}


def playlist_albums(client: Spotify, playlist_id: str) -> List[Dict[str, str]]:
    """"""
    fields = "tracks.items(track(album))"
    playlist = client.playlist(playlist_id, fields=fields)
    songs = playlist["tracks"]["items"]
    return [s["track"]["album"] for s in songs]


def valid_count(album_data: List[Dict[str, str]], album_count: int) -> bool:
    """"""
    if album_count > len(album_data):
        return False
    else:
        return True


def pick_albums(
    client: Spotify,
    album_data: List[Dict[str, str]],
    album_count: int,
    seed: float = None,
) -> List[Dict[str, str]]:
    """"""
    random.seed = seed
    chosen_albums = random.sample(album_data, k=album_count)

    # Get album info for chosen songs
    albums = []
    for album_data in chosen_albums:
        # Put album data dict into albums
        album = {}
        album["name"] = album_data["name"]
        album["artists"] = [a["name"] for a in album_data["artists"]]
        album["image"] = album_data["images"][2]["url"]

        tracks = client.album_tracks(album_data["id"])
        album["songs"] = [track["id"] for track in tracks["items"]]

        albums.append(album)

    return albums


def display_album(album: Dict[str, str]) -> None:
    """"""
    st.image(album["image"])
    st.text(f"Album: {album['name']}")
    st.text(f"By: {', '.join(album['artists'])}")


def add_songs(client: Spotify, output_playlist_id: str, albums: Dict[str, str]) -> None:
    """"""
    songs = []
    for a in albums:
        songs.extend(a["songs"])
    client.playlist_add_items(output_playlist_id, songs)
    st.write(f"Added {', '.join([a['name'] for a in albums])}")
