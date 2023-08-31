import os
from googleapiclient.discovery import build
import json

API_KEY: str = os.environ.get('YT_API_KEY')

class Channel:

    """Класс для YouTube-канала"""

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id

        self.youtube = build('youtube', 'v3', developerKey=API_KEY)

        request = self.youtube.channels().list(part='snippet,statistics', id=self.channel_id).execute()

        self.title = request["items"][0]["snippet"]["title"]
        self.description = request["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + self.channel_id
        self.subscribers_count = int(request["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(request["items"][0]["statistics"]["videoCount"])
        self.view_count = int(request["items"][0]["statistics"]["viewCount"])

    @classmethod
    def get_service(cls):
        """
        возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, ref):
        """
    сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        exemplar_to_json = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers_count": self.subscribers_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(ref, 'w') as file:
            json.dump(exemplar_to_json, file, indent=2, ensure_ascii=False)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        request = self.youtube.channels().list(part='snippet,statistics', id=self.channel_id).execute()
        print(json.dumps(request, indent=2, ensure_ascii=False))



