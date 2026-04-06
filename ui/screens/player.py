import mpv
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label, LoadingIndicator, Static
from textual.containers import Vertical, Center
from textual import work

# Importamos o modelo e a SUA classe de API
from core.models import MusicServer
from core.api.jellyfin_client import FloruneJellyClient

class PlayerScreen(Screen):
    CSS = """
    #player-main {
        width: 100%;
        height: 100%;
    }
    #status-bar {
        background: $surface;
        color: $text;
        padding: 0 1;
        border-bottom: solid $primary;
        height: 1;
    }
    #loading-view {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    .hidden {
        display: none;
    }
    ListItem {
        padding: 0 1;
    }
    """

    def __init__(self, server_data: dict):
        super().__init__()
        self.server_info = server_data
        
        # CORREÇÃO: Usando o nome correto da sua classe de API
        self.client = FloruneJellyClient() 
        self.songs_list = []
        
        # Inicializa o MPV com logs para o terminal (ajuda no debug do CachyOS)
        try:
            self.player = mpv.MPV(ytdl=False, video=False, log_handler=print)
            self.player.volume = 100
        except Exception as e:
            self.player = None
            print(f"Erro ao carregar libmpv: {e}")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Status: [yellow]🟡 Verificando servidor...[/]", id="status-bar")
        
        with Vertical(id="player-main"):
            with Vertical(id="loading-view"):
                yield Center(LoadingIndicator())
                yield Center(Label("[b]Sincronizando Biblioteca...[/]"))
                yield Center(Label(f"[dim]{self.server_info['url']}[/]"))
            
            yield ListView(id="song-list", classes="hidden")
        
        yield Footer()

    async def on_mount(self) -> None:
        self.iniciar_conexao()

    @work(exclusive=True)
    async def iniciar_conexao(self) -> None:
        status_bar = self.query_one("#status-bar", Static)
        try:
            # Chama o método de autenticação que criamos no FloruneJellyClient
            auth_success = self.client.authenticate(
                self.server_info['url'], 
                self.server_info['user'], 
                self.server_info['password']
            )

            if auth_success:
                status_bar.update(f"Status: [green]● Conectado como {self.server_info['user']}[/]")
                # Busca as 100 primeiras músicas reais (sem ser as pastas)
                self.songs_list = self.client.get_tracks(limit=100)
                self.app.call_later(self.exibir_lista)
            else:
                status_bar.update("Status: [red]○ Falha na Autenticação[/]")
                self.notify("Credenciais inválidas!", severity="error")
        except Exception as e:
            status_bar.update("Status: [red]○ Erro de Conexão[/]")
            self.notify(f"Erro: {e}", severity="error")

    def exibir_lista(self) -> None:
        loading_view = self.query_one("#loading-view")
        song_list = self.query_one("#song-list", ListView)

        loading_view.add_class("hidden")
        song_list.remove_class("hidden")

        song_list.clear()
        for song in self.songs_list:
            item = ListItem(
                Label(f"🎵 [b]{song.title}[/] - {song.artist} [dim]({song.album})[/]"), 
                id=f"song-{song.id}"
            )
            song_list.mount(item)
        
        self.notify(f"{len(self.songs_list)} músicas prontas!")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Toca a música ao apertar Enter."""
        index = event.list_view.index
        
        if self.player and index is not None and index < len(self.songs_list):
            selected_song = self.songs_list[index]
            try:
                # O MPV agora recebe a URL completa com o token
                self.player.play(selected_song.stream_url)
                self.notify(f"Tocando: {selected_song.title}")
            except Exception as e:
                self.notify(f"Erro ao tocar: {e}", severity="error")

    def on_unmount(self) -> None:
        if self.player:
            self.player.terminate()