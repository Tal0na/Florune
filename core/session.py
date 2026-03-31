# core/session.py
from .models import MusicServer

class Session:
    def __init__(self):
        self.current_server: MusicServer | None = None
        self.auth_token: str | None = None

    def set_active_server(self, server: MusicServer):
        self.current_server = server
        self.auth_token = server.token