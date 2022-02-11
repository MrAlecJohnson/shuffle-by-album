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
# This playlist contains:
# 2 tracks from album 1, by artist 1
# 1 track from album 2, by artist 2
# 1 track from album 3, by artist 2
playlist_response = {
    "tracks": {
        "items": [
            {
                "track": {
                    "album": {
                        "artists": [{"name": "Test artist"}],
                        "id": "album_id_1",
                        "images": [
                            {"url": "https://i.scdn.co/image/album_1_big"},
                            {"url": "https://i.scdn.co/image/album_1_medium"},
                            {"url": "https://i.scdn.co/image/album_1_small"},
                        ],
                        "name": "Test Album One",
                    }
                }
            },
            {
                "track": {
                    "album": {
                        "artists": [{"name": "Test artist 2"}],
                        "id": "album_id_2",
                        "images": [
                            {"url": "https://i.scdn.co/image/album_2_big"},
                            {"url": "https://i.scdn.co/image/album_2_medium"},
                            {"url": "https://i.scdn.co/image/album_2_small"},
                        ],
                        "name": "Test Album Two",
                    }
                }
            },
            {
                "track": {
                    "album": {
                        "artists": [{"name": "Test artist"}],
                        "id": "album_id_1",
                        "images": [
                            {"url": "https://i.scdn.co/image/album_1_big"},
                            {"url": "https://i.scdn.co/image/album_1_medium"},
                            {"url": "https://i.scdn.co/image/album_1_small"},
                        ],
                        "name": "Test Album One",
                    }
                }
            },
            {
                "track": {
                    "album": {
                        "artists": [{"name": "Test artist 2"}],
                        "id": "album_id_3",
                        "images": [
                            {"url": "https://i.scdn.co/image/album_3_big"},
                            {"url": "https://i.scdn.co/image/album_3_medium"},
                            {"url": "https://i.scdn.co/image/album_3_small"},
                        ],
                        "name": "Test Album Three",
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

    def album_tracks(self, album_id):
        tracks = {
            "album_id_1": [{"id": "song_1"}, {"id": "song_2"}],
            "album_id_3": [{"id": "song_5"}, {"id": "song_6"}],
            "album_id_2": [{"id": "song_3"}, {"id": "song_4"}],
        }
        return {"items": tracks[album_id]}
