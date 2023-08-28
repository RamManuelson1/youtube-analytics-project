import os
from googleapiclient.discovery import build
import json

API_KEY: str = os.environ.get('YT_API_KEY')

class Channel:

    """Класс для YouTube-канала"""

    def __int__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=API_KEY)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        request = self.youtube.channels().list(part='snippet,statistics', id=self.channel_id).execute()
        print(json.dumps(request, indent=2, ensure_ascii=False))

