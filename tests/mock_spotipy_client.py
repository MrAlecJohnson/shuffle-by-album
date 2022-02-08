playlist_data = {
    "href": "https://api.spotify.com/v1/users/mock_user/playlists?offset=0&limit=50",
    "items": [
        {
            "collaborative": False,
            "description": "Test playlist",
            "external_urls": {"spotify": "https://open.spotify.com/playlist/1"},
            "href": "https://api.spotify.com/v1/playlists/1",
            "id": "test_playlist_1",
            "images": [
                {
                    "height": 640,
                    "url": "https://i.scdn.co/image/1",
                    "width": 640,
                }
            ],
            "name": "Test playlist 1",
            "owner": {
                "display_name": "mock_user",
                "external_urls": {"spotify": "https://open.spotify.com/user/mock_user"},
                "href": "https://api.spotify.com/v1/users/mock_user",
                "id": "mock_user",
                "type": "user",
                "uri": "spotify:user:mock_user",
            },
            "primary_color": None,
            "public": False,
            "snapshot_id": "snapshot_string==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/1/tracks",
                "total": 9,
            },
            "type": "playlist",
            "uri": "spotify:playlist:1",
        },
        {
            "collaborative": False,
            "description": "Test playlist 2",
            "external_urls": {"spotify": "https://open.spotify.com/playlist/2"},
            "href": "https://api.spotify.com/v1/playlists/2",
            "id": "test_playlist_2",
            "images": [
                {
                    "height": 640,
                    "url": "https://i.scdn.co/image/2",
                    "width": 640,
                }
            ],
            "name": "Test playlist 2",
            "owner": {
                "display_name": "mock_user",
                "external_urls": {"spotify": "https://open.spotify.com/user/mock_user"},
                "href": "https://api.spotify.com/v1/users/mock_user",
                "id": "mock_user",
                "type": "user",
                "uri": "spotify:user:mock_user",
            },
            "primary_color": None,
            "public": False,
            "snapshot_id": "snapshot_string==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/2/tracks",
                "total": 90,
            },
            "type": "playlist",
            "uri": "spotify:playlist:2",
        },
    ],
    "limit": 50,
    "next": None,
    "offset": 0,
    "previous": None,
    "total": 2,
}


class MockSpotipy:
    def __init__(self):
        self.playlists = playlist_data

    def current_user_playlists(self):
        return self.playlists
