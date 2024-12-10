# Функции для работы с API яндекс музыки

from yandex_music_client import client


def parse_playlist_url(url):
    parts = url.split("/")
    username = parts[4]
    playlist_id = parts[6]
    if "?" in playlist_id:
        playlist_id = playlist_id.split("?")[0]
    return username, playlist_id


def get_songs_by_playlist_url(playlist_url) -> list[dict]:
    username, playlist_id = parse_playlist_url(playlist_url)
    playlist = client.users_playlists(int(playlist_id), username)

    tracks = playlist.tracks
    tracks_full_info = []
    for track in tracks:
        track_info = track.fetch_track()
        tracks_full_info.append(
            {
                "title": track_info.title,
                "artists": ", ".join([artist.name for artist in track_info.artists]),
                "url": f"https://music.yandex.ru/track/{track_info.id}",
            }
        )

    return tracks_full_info
