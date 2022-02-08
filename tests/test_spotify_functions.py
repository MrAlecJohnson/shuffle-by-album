import pytest

from shuffle_by_album.spotify_functions import (
    get_params,
    playlist_id_dict,
    # playlist_albums,
    valid_count,
    # pick_albums,
    # extract_album_info,
    # add_songs,
)
from tests.mock_spotipy_client import MockSpotipy


@pytest.fixture(scope="session")
def mock_client():
    return MockSpotipy()


def test_get_params():
    params = get_params("tests/mock_params.yaml")
    assert params["client_id"] == "mock_id1234"
    assert params["client_secret"] == "mock_secret5678"
    assert params["redirect_uri"] == "http://localhost:8080"


def test_playlist_id_dict(mock_client):
    assert playlist_id_dict(mock_client) == {
        "Test playlist 1": "test_playlist_1",
        "Test playlist 2": "test_playlist_2",
    }


@pytest.mark.parametrize(
    "album_ids, album_count, expected",
    [
        ([1], 1, True),
        ([1, 2, 3, 4], 4, True),
        ([1, 1, 2, 2], 2, True),
        ([], 1, False),
        ([1, 2], 3, False),
        ([1, 1, 2, 2], 3, False),
    ],
)
def test_valid_count(album_ids, album_count, expected):
    album_data = [{"id": num} for num in album_ids]
    assert valid_count(album_data, album_count) == expected
