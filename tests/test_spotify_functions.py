from shuffle_by_album.spotify_functions import valid_count


def test_valid_count():
    assert valid_count([{"id": 1}], 1)
