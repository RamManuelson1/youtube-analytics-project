from datetime import timedelta
from src.video import Video
import isodate

class PlayList(Video):
    """класс для плейлиста"""
    def __init__(self, playlist_id) -> None:
        playlist = super().get_service().playlists().list(id=playlist_id, part="id, snippet").execute()

        self.playlist_id = playlist_id
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist['items'][0]['id']}"
        playlist_video = super().get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResult=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_video['items']]
        self.video_response = super().get_service().videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

    def __str__(self):
        return self.title

    @property
    def playlist_id(self):
        return self.playlist_id

    @playlist_id.setter
    def playlist_id(self, value):
        self.playlist_id = value

    @property
    def total_duration(self):
        """
        возвращает продолжительность всего плейлиста
        """
        total_duration = 0

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration).seconds
            total_duration += duration

        return timedelta(seconds=total_duration)

    def show_best_video(self):
        """
        ссылка на самое популярное видео плейлиста
        """
        max_likes: int = 0
        bests_video: str = ''

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_likes:
                max_likes = int(video['statistics']['likeCount'])
                bests_video = video['id']
        return f"https://youtu.be/{bests_video}"