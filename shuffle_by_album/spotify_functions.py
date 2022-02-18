import random
from typing import Dict, List

from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth


class NotEnoughAlbums(Exception):
    pass


def authenticate_spotify(
    client_id: str, client_secret: str, redirect_uri: str
) -> SpotifyOAuth:
    """Authenticate with the Spotify API.

    Parameters
    ----------
    client_id : str
        Developer client id for the Spotify app.
    client_secret : str
        Developer client secret for the Spotify app.
    redirect_uri : str
        Spotify demands this but not sure I understand it yet.
        Works fine as "http://localhost:8080"

    Returns
    -------
    SpotifyOAuth
        An authentication token you can pass to the auth_manager parameter
        when creating a Spotify client with spotipy.Spotify()
    """
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-modify-private",
    )


def playlist_id_dict(client: Spotify) -> Dict[str, str]:
    """Get name and corresponding ID for each of the user's private playlists.

    Parameters
    ----------
    client : Spotify
        A Spotify client loaded with create_spotify_client

    Returns
    -------
    dict
        Dictionary where each key is a playlist name and each value that playlist's id
    """
    playlists = client.current_user_playlists()["items"]
    return {p["name"]: p["id"] for p in playlists}


def playlist_albums(client: Spotify, playlist_id: str) -> List[Dict[str, str]]:
    """For each track on a playlist, get information about the album it's from.

    Allows repeat albums, as a crude way to enable weighting the probabilities.

    Parameters
    ----------
    client : Spotify
        A Spotify client loaded with create_spotify_client
    playlist_id : str
        ID of the playlist to operate on

    Returns
    -------
    list
        A dictionary for each song, containing all the information the API has returned
        on the album that song comes from.
    """
    fields = "tracks.items(track(album))"
    playlist = client.playlist(playlist_id, fields=fields)
    songs = playlist["tracks"]["items"]
    return [s["track"]["album"] for s in songs]


def valid_count(album_data: List[Dict[str, str]], album_count: int) -> bool:
    """Check if the user has asked for more albums than the playlist contains.

    Only counts unique albums in the playlist.

    Parameters
    ----------
    album_data : list
        List of dictionaries containing album information, as returned by
        playlist_albums.
    album_count : int
        The number of unique albums the user has requested.

    Returns
    -------
    bool
        True if the playlist contains enough albums to meet the user request.
    """
    unique_count = len(set([a["id"] for a in album_data]))
    if album_count <= unique_count:
        return True
    else:
        raise NotEnoughAlbums(
            (
                f"You asked for {album_count} albums, but "
                f"this playlist only contains {unique_count}"
            )
        )


def pick_albums(
    album_data: List[Dict[str, str]],
    album_count: int,
    seed: float = None,
) -> List[Dict[str, str]]:
    """Pick a sample of unique albums, weighted by number of times each album appears.

    Use valid_count first to check enough albums are available.

    Parameters
    ----------
    album_data : list
        List of dictionaries of album information created with playlist_albums.
    album_count : int
        Number of unique albums to pick from the data.
    seed : float
        Seed value to pass to random number generator for replicable results.

    Returns
    -------
    list
        Dictionary of information for each of the selected albums.
    """
    valid_count(album_data, album_count)
    random.seed(seed)
    # Can't just bung it into a set because dictionaries aren't hashable
    # But album ids are hashable, so pick from them and add to a set
    # Not using random sample because I want to weight by number of appearances
    # Could probably do with numpy.choices instead
    album_ids = [a["id"] for a in album_data]
    chosen_ids = set()
    while len(chosen_ids) < album_count:
        chosen_ids.add(random.choice(album_ids))

    # Now turn chosen ids back into full album info
    album_dict = {a["id"]: a for a in album_data}
    return [album_dict[c] for c in chosen_ids]


def extract_album_info(
    client: Spotify, chosen_albums: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Pare down a list of chosen albums to just the display information and track list.

    Parameters
    ----------
    client : Spotify
        A Spotify client loaded with create_spotify_client.
    chosen_albums : list
        List of the selected albums, created with playlist_albums and pick_albums.

    Returns
    -------
    list
        Reduced dictionaries for the albums, including just name, artist names, cover
        image link and list of track ids.
    """
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


def add_songs(
    client: Spotify, output_playlist_id: str, albums: List[Dict[str, str]]
) -> None:
    """Add all songs from all albums in a list to a given Spotify playlist.

    Parameters
    ----------
    client : Spotify
        A Spotify client loaded with create_spotify_client.
    output_playlist_id : str
        ID of the playlist to add the songs to.
    albums : list
        List of albums to add, created with extract_album_info.

    Returns
    -------
    None
        Changes all happen directly on Spotify through the API.
    """
    songs = []
    for a in albums:
        songs.extend(a["songs"])
    client.playlist_add_items(output_playlist_id, songs)
