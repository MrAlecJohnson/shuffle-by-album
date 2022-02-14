from typing import Dict, List

from spotipy.client import Spotify
import streamlit as st

from shuffle_by_album.spotify_functions import playlist_id_dict, add_songs


@st.cache
def cache_playlists(client: Spotify) -> Dict[str, str]:
    """Run playlist_id_dict, but cache the results so Streamlit doesn't reload them.

    Wrapper so the base function can run independently in unit tests and notebooks.

    Parameters
    ----------
    client : Spotify
        A Spotify client loaded with create_spotify_client

    Returns
    -------
    dict
        Dictionary where each key is a playlist name and each value that playlist's id
    """
    return playlist_id_dict(client)


def reset_album_choices():
    """Callback to reset album choices and info to None when you change inputs."""
    st.session_state.albums = None
    st.session_state.album_info = None


def display_album(album: Dict[str, str]) -> None:
    """Use Streamlit to display an album's cover image, name and artist names.

    Parameters
    ----------
    album : dict
        Dictionary of pared down album information - an item from the list created by
        extract_album_info.

    Returns
    -------
    None
        Just displays the relevant data in a browser.
    """
    st.image(album["image"])
    st.text(f"Album: {album['name']}")
    st.text(f"By: {', '.join(album['artists'])}")


def add_and_print_songs(
    client: Spotify, output_playlist_id: str, albums: List[Dict[str, str]]
) -> None:
    """Add all songs from all albums in a list to a given Spotify playlist.
    Print a message describing the changes in Streamlit.

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
    add_songs(client, output_playlist_id, albums)
    st.write(f"Added {', '.join([a['name'] for a in albums])}")


def submit_button(client: Spotify) -> None:
    """Streamlit button wrapped around add_and_print_songs."""
    if st.button("Add to playlist"):
        if st.session_state.album_info:
            add_and_print_songs(
                client, st.session_state.output_playlist_id, st.session_state.album_info
            )
            reset_album_choices()
        else:
            st.write("Pick one or more albums first")
