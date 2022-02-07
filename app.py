import spotipy
import streamlit as st

from shuffle_by_album.spotify_functions import (
    authenticate_spotify,
    get_params,
    playlist_albums,
    pick_albums,
    extract_album_info,
    valid_count,
)
from shuffle_by_album.streamlit_functions import (
    cache_playlists,
    display_album,
    add_and_print_songs,
)
from shuffle_by_album.constants import title

params = get_params("params.yaml")
auth = authenticate_spotify(params)
sp = spotipy.Spotify(auth_manager=auth)


def main():
    playlists = cache_playlists(sp)

    # Initialise session variables
    if "input_playlist_id" not in st.session_state:
        st.session_state.input_playlist_id = None
    if "output_playlist_id" not in st.session_state:
        st.session_state.output_playlist_id = None
    if "album_count" not in st.session_state:
        st.session_state.album_count = 1
    if "albums" not in st.session_state:
        st.session_state.albums = []
    if "album_info" not in st.session_state:
        st.session_state.album_info = []

    # Sidebar
    input_playlist_name = st.sidebar.selectbox(
        "Which playlist do you want albums from?", playlists.keys()
    )
    if input_playlist_name:
        st.session_state.input_playlist_id = playlists[input_playlist_name]

    st.session_state.album_count = st.sidebar.slider(
        "How many albums would you like to pick?", 1, 10, value=1
    )

    output_playlist_name = st.sidebar.selectbox(
        "Which playlist do you want to add the albums to?", playlists.keys()
    )
    if output_playlist_name:
        st.session_state.output_playlist_id = playlists[output_playlist_name]

    potential_albums = playlist_albums(sp, st.session_state.input_playlist_id)

    #  Main panel
    st.title(title)

    if st.button("Pick albums"):
        if valid_count(potential_albums, st.session_state.album_count):
            st.session_state.albums = pick_albums(
                potential_albums, st.session_state.album_count
            )
            st.session_state.album_info = extract_album_info(
                sp, st.session_state.albums
            )
            "Albums chosen"
            for a in st.session_state.album_info:
                display_album(a)

        else:
            st.session_state.albums = []
            (
                f"The selected playlist isn't long enough to pick "
                f"{st.session_state.album_count} albums"
            )

    if st.button("Add to playlist"):
        if st.session_state.albums:
            add_and_print_songs(
                sp, st.session_state.output_playlist_id, st.session_state.albums
            )
        else:
            "Pick one or more albums first"


if __name__ == "__main__":
    main()
