from googleapiclient.discovery import build

import os

API_KEY: str = os.environ.get('YT_API_KEY')

class Video:
    """
    Класс для Ютуб видео
    """
    def __init__(self, id_video: str) -> None:
        self.id_video = id_video


        try:

            request = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',id=id_video).execute()

            self.title: str = request["items"][0]["snippet"]["title"]
            self.video_url: str = f"https://www.youtube.com/watch?v={self.id_video}"
            self.count_viev: int = request['items'][0]['statistics']['viewCount']
            self.count_like: int = request['items'][0]['statistics']['likeCount']

        except IndexError as e:
            print(f'Ошибка: {e}')
            self.title = None
            self.video_url = None
            self.count_viev = None
            self.count_like = None

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)

class PLVideo(Video):
    def __init__(self, id_video: str, id_playlist: str) -> None:
        super().__init__(id_video)
        self.id_playlist = id_playlist