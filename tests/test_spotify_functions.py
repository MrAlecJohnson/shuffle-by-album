import pytest

from shuffle_by_album.spotify_functions import (
    NotEnoughAlbums,
    playlist_id_dict,
    playlist_albums,
    valid_count,
    pick_albums,
    extract_album_info,
)
from tests.mock_spotipy_client import MockSpotipy


@pytest.fixture(scope="session")
def mock_client():
    return MockSpotipy()


@pytest.fixture(scope="session")
def album_data():
    return [
        {
            "artists": [{"name": "Test artist"}],
            "id": "album_id_1",
            "images": [
                {"url": "https://i.scdn.co/image/album_1_big"},
                {"url": "https://i.scdn.co/image/album_1_medium"},
                {"url": "https://i.scdn.co/image/album_1_small"},
            ],
            "name": "Test Album One",
        },
        {
            "artists": [{"name": "Test artist 2"}],
            "id": "album_id_2",
            "images": [
                {"url": "https://i.scdn.co/image/album_2_big"},
                {"url": "https://i.scdn.co/image/album_2_medium"},
                {"url": "https://i.scdn.co/image/album_2_small"},
            ],
            "name": "Test Album Two",
        },
        {
            "artists": [{"name": "Test artist"}],
            "id": "album_id_1",
            "images": [
                {"url": "https://i.scdn.co/image/album_1_big"},
                {"url": "https://i.scdn.co/image/album_1_medium"},
                {"url": "https://i.scdn.co/image/album_1_small"},
            ],
            "name": "Test Album One",
        },
        {
            "artists": [{"name": "Test artist 2"}],
            "id": "album_id_3",
            "images": [
                {"url": "https://i.scdn.co/image/album_3_big"},
                {"url": "https://i.scdn.co/image/album_3_medium"},
                {"url": "https://i.scdn.co/image/album_3_small"},
            ],
            "name": "Test Album Three",
        },
    ]


def test_playlist_id_dict(mock_client):
    assert playlist_id_dict(mock_client) == {
        "Test playlist 1": "test_playlist_1",
        "Test playlist 2": "test_playlist_2",
    }


def test_playlist_albums(mock_client, album_data):
    result = playlist_albums(mock_client, "not tested")
    assert result == album_data


@pytest.mark.parametrize(
    "album_ids, album_count, expected, unique_count",
    [
        ([1], 1, True, 1),
        ([1, 2, 3, 4], 4, True, 4),
        ([1, 1, 2, 2], 2, True, 2),
        ([], 1, False, 0),
        ([1, 2], 3, False, 2),
        ([1, 1, 2, 2], 3, False, 2),
    ],
)
def test_valid_count(album_ids, album_count, expected, unique_count):
    album_data = [{"id": num} for num in album_ids]
    if expected:
        assert valid_count(album_data, album_count) == expected
    else:
        expected_error = (
            f"You asked for {album_count} albums, but "
            f"this playlist only contains {unique_count}"
        )
        with pytest.raises(NotEnoughAlbums, match=expected_error):
            valid_count(album_data, album_count)


@pytest.mark.parametrize(
    "album_count, seed, expected",
    [
        # Get 4 unique albums when there are only 3
        (4, 100, "ERROR"),
        # Get 1
        (
            1,
            100,
            [
                {
                    "artists": [{"name": "Test artist 2"}],
                    "id": "album_id_2",
                    "images": [
                        {"url": "https://i.scdn.co/image/album_2_big"},
                        {"url": "https://i.scdn.co/image/album_2_medium"},
                        {"url": "https://i.scdn.co/image/album_2_small"},
                    ],
                    "name": "Test Album Two",
                }
            ],
        ),
        # Get 1 with another seed
        (
            1,
            50,
            [
                {
                    "artists": [{"name": "Test artist 2"}],
                    "id": "album_id_3",
                    "images": [
                        {"url": "https://i.scdn.co/image/album_3_big"},
                        {"url": "https://i.scdn.co/image/album_3_medium"},
                        {"url": "https://i.scdn.co/image/album_3_small"},
                    ],
                    "name": "Test Album Three",
                }
            ],
        ),
        # Get them all
        (
            3,
            100,
            [
                {
                    "artists": [{"name": "Test artist"}],
                    "id": "album_id_1",
                    "images": [
                        {"url": "https://i.scdn.co/image/album_1_big"},
                        {"url": "https://i.scdn.co/image/album_1_medium"},
                        {"url": "https://i.scdn.co/image/album_1_small"},
                    ],
                    "name": "Test Album One",
                },
                {
                    "artists": [{"name": "Test artist 2"}],
                    "id": "album_id_2",
                    "images": [
                        {"url": "https://i.scdn.co/image/album_2_big"},
                        {"url": "https://i.scdn.co/image/album_2_medium"},
                        {"url": "https://i.scdn.co/image/album_2_small"},
                    ],
                    "name": "Test Album Two",
                },
                {
                    "artists": [{"name": "Test artist 2"}],
                    "id": "album_id_3",
                    "images": [
                        {"url": "https://i.scdn.co/image/album_3_big"},
                        {"url": "https://i.scdn.co/image/album_3_medium"},
                        {"url": "https://i.scdn.co/image/album_3_small"},
                    ],
                    "name": "Test Album Three",
                },
            ],
        ),
    ],
)
def test_pick_albums(album_count, seed, expected, album_data):
    if expected == "ERROR":
        with pytest.raises(NotEnoughAlbums):
            pick_albums(album_data, album_count, seed)
    else:
        # Sort result because function uses sets
        result = pick_albums(album_data, album_count, seed)
        assert sorted(result, key=lambda x: x["id"]) == expected


def test_extract_album_info(mock_client, album_data):
    chosen_albums = album_data[0:2]
    assert extract_album_info(mock_client, chosen_albums) == [
        {
            "name": "Test Album One",
            "artists": ["Test artist"],
            "image": "https://i.scdn.co/image/album_1_small",
            "songs": ["song_1", "song_2"],
        },
        {
            "name": "Test Album Two",
            "artists": ["Test artist 2"],
            "image": "https://i.scdn.co/image/album_2_small",
            "songs": ["song_3", "song_4"],
        },
    ]
