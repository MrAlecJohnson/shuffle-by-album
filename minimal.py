import os

from dotenv import load_dotenv
import spotipy
import streamlit as st

from shuffle_by_album.spotify_functions import authenticate_spotify
from shuffle_by_album.streamlit_functions import initialise_variables
from shuffle_by_album.constants import redirect_uri


def app_sign_in():
    sp = spotipy.Spotify(auth=st.session_state["cached_token"])
    st.session_state["signed_in"] = True
    st.success("Signed in successfully")
    return sp


def get_token(oauth, code):
    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    # Remove cached token
    os.remove(".cache")

    # Return the token
    return token


def app_get_token():
    token = get_token(st.session_state["oauth"], st.session_state["code"])
    st.session_state["cached_token"] = token


def main():
    st.title("This is a title")
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    variables = ["signed_in", "cached_token", "code", "oauth"]
    values = [False, "", "", None]
    initialise_variables(variables, values)

    url_params = st.experimental_get_query_params()

    # Try to sign in with cached token
    if st.session_state["cached_token"]:
        print("Cached token")
        pass
    # If no token, but code in url, get code, parse token, and sign in
    elif "code" in url_params:
        print("Code in url")
        st.session_state["code"] = url_params["code"][0]
        app_get_token()

    # Authenticate
    auth = authenticate_spotify(client_id, client_secret, redirect_uri)
    # Store oauth in session
    st.session_state["oauth"] = auth
    print(st.session_state["oauth"])

    if not st.session_state["signed_in"]:
        print("Not signed in")
        # Retrieve auth url
        auth_url = auth.get_authorize_url()
        link_html = f'<a target="_self" href="{auth_url}" >Click to log in</a>'
        print(link_html)
        st.markdown(link_html, unsafe_allow_html=True)

    else:
        print("Signing in")
        sp = app_sign_in()

        # Do stuff
        # st.write(playlist_id_dict(sp).keys())


if __name__ == "__main__":
    main()
