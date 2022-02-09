playlists_response = {
    "href": "https://api.spotify.com/v1/users/mock_user/playlists?offset=0&limit=50",
    "items": [
        {
            "id": "test_playlist_1",
            "name": "Test playlist 1",
        },
        {
            "id": "test_playlist_2",
            "name": "Test playlist 2",
        },
    ],
    "total": 2,
}
playlist_response = {
    "tracks": {
        "items": [
            {
                "track": {
                    "album": {
                        "artists": [
                            {
                                "name": "Test artist",
                            }
                        ],
                        "id": "album_id_1",
                        "images": [
                            {
                                "height": 640,
                                "url": "https://i.scdn.co/image/album_1_big",
                                "width": 640,
                            },
                            {
                                "height": 300,
                                "url": "https://i.scdn.co/image/album_1_medium",
                                "width": 300,
                            },
                            {
                                "height": 64,
                                "url": "https://i.scdn.co/image/album_1_small",
                                "width": 64,
                            },
                        ],
                        "name": "Test Album One",
                    }
                }
            },
            {
                "track": {
                    "album": {
                        "artists": [
                            {
                                "name": "Test artist 2",
                            }
                        ],
                        "id": "album_id_2",
                        "images": [
                            {
                                "height": 640,
                                "url": "https://i.scdn.co/image/album_2_big",
                                "width": 640,
                            },
                            {
                                "height": 300,
                                "url": "https://i.scdn.co/image/album_2_medium",
                                "width": 300,
                            },
                            {
                                "height": 64,
                                "url": "https://i.scdn.co/image/album_2_small",
                                "width": 64,
                            },
                        ],
                        "name": "Test Album Two",
                    }
                }
            },
        ]
    }
}


class MockSpotipy:
    def __init__(self):
        self.playlists_response = playlists_response
        self.playlist_response = playlist_response

    def current_user_playlists(self):
        return self.playlists_response

    def playlist(self, playlist_id, fields):
        return self.playlist_response
