import spotipy
import streamlit as st

from shuffle_by_album.spotify_functions import (
    NotEnoughAlbums,
    authenticate_spotify,
    get_params,
    playlist_albums,
    pick_albums,
    extract_album_info,
)
from shuffle_by_album.streamlit_functions import (
    cache_playlists,
    display_album,
    submit_button,
    reset_album_choices,
)
from shuffle_by_album.constants import title, params_filename

params = get_params(params_filename)
auth = authenticate_spotify(params)
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
    input_playlist_name = st.sidebar.selectbox(
        "Which playlist do you want albums from?",
        playlists.keys(),
        on_change=reset_album_choices,
    )
    if input_playlist_name:
        st.session_state.input_playlist_id = playlists[input_playlist_name]

    st.session_state.album_count = st.sidebar.slider(
        "How many albums would you like to pick?",
        1,
        10,
        value=1,
        on_change=reset_album_choices,
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
        try:
            st.session_state.albums = pick_albums(
                potential_albums, st.session_state.album_count
            )
            st.session_state.album_info = extract_album_info(
                sp, st.session_state.albums
            )
            "Albums chosen"
            for a in st.session_state.album_info:
                display_album(a)

        except NotEnoughAlbums as e:
            st.session_state.albums = []
            st.write(str(e))

    submit_button(sp)


if __name__ == "__main__":
    main()
