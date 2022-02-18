from os import getenv

from dotenv import load_dotenv
import spotipy
import streamlit as st

from shuffle_by_album.spotify_functions import (
    authenticate_spotify,
    playlist_albums,
)
from shuffle_by_album.streamlit_functions import (
    cache_playlists,
    input_playlist_picker,
    album_count_slider,
    output_playlist_picker,
    album_picker_button,
    submit_button,
)
from shuffle_by_album.constants import title, redirect_uri


load_dotenv()
client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")

auth = authenticate_spotify(client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(auth_manager=auth)

# Initialise session variables
variables = [
    "input_playlist_id",
    "output_playlist_id",
    "album_count",
    "albums",
    "album_info",
]
for v in variables:
    if v not in st.session_state:
        setattr(st.session_state, v, None)


def main():
    playlists = cache_playlists(sp)

    # Sidebar
    input_playlist_name = input_playlist_picker(playlists)
    if input_playlist_name:
        st.session_state.input_playlist_id = playlists[input_playlist_name]
        potential_albums = playlist_albums(sp, st.session_state.input_playlist_id)

    st.session_state.album_count = album_count_slider()

    output_playlist_name = output_playlist_picker(playlists)
    if output_playlist_name:
        st.session_state.output_playlist_id = playlists[output_playlist_name]

    #  Main panel
    st.title(title)
    album_picker_button(sp, potential_albums)
    submit_button(sp)


if __name__ == "__main__":
    main()
