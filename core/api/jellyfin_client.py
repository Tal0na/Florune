from jellyfin_apiclient_python import JellyfinClient
from core.models import Song

class FloruneJellyClient:
    def __init__(self):
        # Instancia o cliente principal
        self.client = JellyfinClient()
        # Configuração obrigatória para identificação no servidor
        self.client.config.app(
            'Florune', '0.1.0', 'CachyOS-Machine', 'florune-id-01'
        )
        # Referências que vamos usar depois
        self.user_id = None
        self.access_token = None
        self.server_url = None

    def authenticate(self, url: str, username: str, password: str) -> bool:
        """Realiza o login e prepara a sessão."""
        try:
            self.server_url = url.rstrip('/')
            
            # 1. Conecta ao endereço (isso configura internamente o ConnectionManager)
            self.client.auth.connect_to_address(self.server_url)
            
            # 2. Realiza o login
            # A biblioteca preenche o AccessToken e User_Id automaticamente no objeto auth
            result = self.client.auth.login(self.server_url, username, password)
            
            if "AccessToken" in result:
                self.access_token = result["AccessToken"]
                self.user_id = result["SessionInfo"]["UserId"]
                return True
            return False
            
        except Exception as e:
            # Em produção, você pode usar o self.notify do Textual aqui passando o erro
            print(f"Erro na conexão Jellyfin: {e}")
            return False

    def get_tracks(self, limit: int = 100):
        if not self.user_id:
            return []

        params = {
            'UserIds': self.user_id,
            'Recursive': True,
            'IncludeItemTypes': 'Audio', # Garante que só venha áudio
            'ExcludeLocationTypes': 'Virtual', # Ignora pastas virtuais/bibliotecas
            'Limit': limit,
            'Fields': 'SortName,RunTimeTicks',
            'SortBy': 'SortName',
            'Recursive': True
        }
        
       # Adicione o user_id dentro do dicionário de parâmetros
        params['UserIds'] = self.user_id

# Chame o método passando APENAS o dicionário params
        data = self.client.jellyfin.get_items(params)
        
        songs = []
        for item in data.get('Items', []):
            # Conversão de Ticks (Jellyfin) para segundos
            # 1 segundo = 10.000.000 de ticks
            ticks = item.get("RunTimeTicks", 0)
            duration_secs = int(ticks / 10_000_000) if ticks else 0
            
            songs.append(Song(
                id=item['Id'],
                title=item['Name'],
                artist=item.get('Artists', ['Desconhecido'])[0],
                album=item.get('Album', 'Sem Álbum'),
                duration=duration_secs,
                # URL de Stream pronta para uso com o Token
                stream_url=f"{self.server_url}/Audio/{item['Id']}/stream?api_key={self.access_token}"
            ))
        return songs