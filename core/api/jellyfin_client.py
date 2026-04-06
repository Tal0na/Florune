from jellyfin_apiclient_python import JellyfinClient
from core.models import Song

class FloruneJellyClient:
    def __init__(self):
        self.client = JellyfinClient()
        self.client.config.app(
            'Florune', '0.1.0', 'CachyOS-Machine', 'florune-id-01'
        )
        self.user_id = None
        self.access_token = None
        self.server_url = None

    def authenticate(self, url: str, username: str, password: str) -> bool:
        """Realiza o login e prepara a sessão."""
        try:
            self.server_url = url.rstrip('/')
            self.client.auth.connect_to_address(self.server_url)
            
            result = self.client.auth.login(self.server_url, username, password)
            
            if "AccessToken" in result:
                self.access_token = result["AccessToken"]
                self.user_id = result["SessionInfo"]["UserId"]
                return True
            return False
        except Exception as e:
            print(f"Erro na conexão Jellyfin: {e}")
            return False

    def get_tracks(self, limit: int = 300):
        if not self.user_id:
            return []

        # Vamos simplificar ao máximo para o Jellyfin não se perder
        params = {
            'UserIds': self.user_id,
            'IncludeItemTypes': 'Audio',  # Mantemos apenas Audio
            'Recursive': True,            # Vasculha todas as subpastas
            'Fields': 'SortName,RunTimeTicks,Album,Artists',
            'SortBy': 'SortName',
            'Limit': limit,
            # 'StartIndex': 0, # Opcional: para paginação futura
        }
        
        try:
            # DEBUG: Imprime no terminal o que está acontecendo
            print(f"Buscando músicas para o usuário: {self.user_id}")
            
            data = self.client.jellyfin.get_items(params)
            items = data.get('Items', [])
            
            print(f"Itens encontrados pelo Jellyfin: {len(items)}")
            
            songs = []
            for item in items:
                # Verificação de segurança para o modelo Song
                ticks = item.get("RunTimeTicks", 0)
                duration = int(ticks / 10_000_000) if ticks else 0
                
                # Pegamos o primeiro artista da lista ou "Desconhecido"
                artists = item.get('Artists', [])
                artist_name = artists[0] if artists else "Artista Desconhecido"

                songs.append(Song(
                    id=item['Id'],
                    title=item.get('Name', 'Sem Título'),
                    artist=artist_name,
                    album=item.get('Album', 'Sem Álbum'),
                    duration=duration,
                    stream_url=f"{self.server_url}/Audio/{item['Id']}/stream?api_key={self.access_token}"
                ))
            
            return songs
        except Exception as e:
            print(f"Erro na API Jellyfin: {e}")
            return []