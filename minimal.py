from os import getenv

from dotenv import load_dotenv
import spotipy
import streamlit as st

from shuffle_by_album.spotify_functions import (
    authenticate_spotify,
)
from shuffle_by_album.constants import redirect_uri


def main():
    st.title("This is a title")
    load_dotenv()
    client_id = getenv("CLIENT_ID")
    client_secret = getenv("CLIENT_SECRET")

    auth = authenticate_spotify(client_id, client_secret, redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth)
    print(sp)


if __name__ == "__main__":
    main()
