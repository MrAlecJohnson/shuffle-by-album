from typing import Dict, List, Any

from spotipy.client import Spotify
import streamlit as st

from shuffle_by_album.spotify_functions import (
    playlist_id_dict,
    add_songs,
    pick_albums,
    extract_album_info,
    NotEnoughAlbums,
)


# UTILS
def initialise_variables(
    variables: List[str], initial_values: List[Any] = None
) -> None:
    """Add variables in list to st.session_state.
    If no initial_values, all will start with value of None.
    If initial_values is list of equal length to variables, map its values to those
    session_variables

    Parameters
    ----------
    variables : list
        Names of the variables to add to st.session_state
    initial_values : list (optional)
        List of equal length to variables.
    """
    if initial_values:
        for i, v in enumerate(variables):
            if v not in st.session_state:
                setattr(st.session_state, v, initial_values[i])
    else:
        for v in variables:
            if v not in st.session_state:
                setattr(st.session_state, v, None)


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


# SIDEBAR INPUT
def input_playlist_picker(playlists: Dict[str, str]) -> str:
    return st.sidebar.selectbox(
        "Which playlist do you want albums from?",
        playlists.keys(),
        on_change=reset_album_choices,
    )


def album_count_slider() -> int:
    return st.sidebar.slider(
        "How many albums would you like to pick?",
        1,
        10,
        value=1,
        on_change=reset_album_choices,
    )


def output_playlist_picker(playlists: Dict[str, str]) -> str:
    return st.sidebar.selectbox(
        "Which playlist do you want to add the albums to?", playlists.keys()
    )


# MAIN DISPLAY
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


def album_picker_button(client: Spotify, potential_albums: List[Dict[str, str]]):
    if st.button("Pick albums"):
        try:
            st.session_state.albums = pick_albums(
                potential_albums, st.session_state.album_count
            )
            st.session_state.album_info = extract_album_info(
                client, st.session_state.albums
            )
            st.write("Albums chosen")
            for a in st.session_state.album_info:
                display_album(a)

        except NotEnoughAlbums as e:
            st.session_state.albums = []
            st.write(str(e))


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
