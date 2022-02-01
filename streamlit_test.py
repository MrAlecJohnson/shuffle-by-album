import random

import spotipy
import streamlit as st

from functions import get_params, log_in

title = "Shuffle by album"

params = get_params("params.yaml")
auth = log_in(params)
sp = spotipy.Spotify(auth_manager=auth)


if __name__ == "__main__":
    playlists = sp.current_user_playlists()["items"]
    playlist_name_id = {p["name"]: p["id"] for p in playlists}

    # Sidebar
    choose_input_playlist = st.sidebar.selectbox(
        "Which playlist do you want albums from?", playlist_name_id.keys()
    )
    input_playlist = playlist_name_id[choose_input_playlist]
    album_count = st.sidebar.slider(
        "How many albums would you like to listen to?", 1, 10, value=1
    )
    choose_output_playlist = st.sidebar.selectbox(
        "Which playlist do you want to add the albums to?", playlist_name_id.keys()
    )
    output_playlist = playlist_name_id[choose_output_playlist]

    fields = "tracks.items(track(album))"
    playlist = sp.playlist(input_playlist, fields=fields)
    input_songs = playlist["tracks"]["items"]

    # Pick 1 or more songs from it to decide which albums to add
    random.seed = None
    chosen_songs = random.choices(input_songs, k=album_count)

    # Get songs from the albums chosen
    song_list = []
    album_list = []
    for song in chosen_songs:
        album_info = song["track"]["album"]
        album_id = album_info["id"]
        album_tracks = sp.album_tracks(album_id)
        album_track_ids = [track["id"] for track in album_tracks["items"]]
        song_list.extend(album_track_ids)
        album_list.append(album_info)

    #  Main panel (how to separate layout from code?)
    title
    album_list
    if st.button("Add to playlist"):
        sp.playlist_add_items(output_playlist, song_list)
