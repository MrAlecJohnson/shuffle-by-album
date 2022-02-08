# shuffle-by-album
Use songs from a playlist to pick a new random playlist of whole albums.

In Spotify I like to play whole albums, but I sometimes want to pick that album at random. Usually I put on a playlist and then when a song takes my fancy I click through to its album.

This automates that process by randomly picking albums based on the songs in a playlist.

This also avoids using Spotify's unclear shuffling algorithm, which *seems* to lean towards things you've played most recently.

## Developer setup

Create a new virtual environment for Python 3.9.6+

Create a file called `params.yaml`, based on the structure in `sample_params.yaml`. This will let you authenticate with Spotify. You'll need to set up a Spotify app first. No docs on this as I plan to have it working as a proper app for multiple users before that becomes relevant.

In Spotify itself, create the playlist you want to pick songs from. Or use an existing one. Either is fine.

Also create a playlist that you want to add your randomly chosen albums to. It doesn't have to be empty.

Then run:

- `pip install -r requirements.txt`
- `pip install -e .` (local install of the package to allow imports)
- `pip install pre-commit`
- `pre-commit install`

To run the app locally: `streamlit run app.py`
