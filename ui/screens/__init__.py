import mpv  # Resolve o erro de "mpv não está definido"
from textual.screen import Screen
from core.api.jellyfin_client import FloruneJellyClient  # Resolve o erro da API

class PlayerScreen(Screen):
    def __init__(self, server_data: dict):
        super().__init__()  # Isso deve estar identado dentro do método!
        self.server_info = server_data
        self.client = FloruneJellyClient()
        self.player = mpv.MPV(ytdl=False, video=False)
        