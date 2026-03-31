from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static, Button
from textual.containers import Vertical, Horizontal
from core.config import ConfigManager

class Dashboard(Screen):
    CSS = """
    #main { layout: grid; grid-size: 2; grid-columns: 1fr 2fr; }
    #left { border-right: tall $accent; padding: 1; }
    #right { padding: 2; align: center middle; }
    .hidden { display: none; }
    #btn-logout { margin-top: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            with Vertical(id="left"):
                yield Label("[b]SERVIDORES[/b]")
                yield ListView(id="server-list")
                yield Button("Adicionar", variant="primary", id="add-server")
                yield Button("Sair/Trocar", variant="error", id="btn-logout")
            
            with Vertical(id="right"):
                yield Static("Selecione um servidor...", id="info")
                yield Button("CONECTAR", variant="success", id="connect-btn", classes="hidden")
        yield Footer()

    def on_mount(self) -> None:
        self.config = ConfigManager()
        self.atualizar_lista()

    def atualizar_lista(self) -> None:
        lista = self.query_one("#server-list", ListView)
        lista.clear()
        for i, s in enumerate(self.config.get_all_active()):
            lista.mount(ListItem(Label(f"Srv: {s['name']}"), id=f"s-{i}"))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if not event.item or not event.item.id:
            return
        try:
            idx = int(event.item.id.split("-")[1])
            srv = self.config.get_all_active()[idx]
            self.query_one("#info", Static).update(f"Conectar em: [cyan]{srv['url']}[/cyan]\nUsuário: [y]{srv['user']}[/y]")
            self.query_one("#connect-btn").remove_class("hidden")
        except:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "connect-btn":
            list_view = self.query_one("#server-list", ListView)
            
            # 1. Verificamos se existe um filho destacado e se ele tem um ID
            target = list_view.highlighted_child
            if target is not None and target.id is not None:
                try:
                    # 2. Fazemos o split apenas se tivermos certeza que o ID existe
                    parts = target.id.split("-")
                    if len(parts) >= 2:
                        idx = int(parts[1])
                        server = self.config.get_all_active()[idx]
                        
                        # 3. Muda para a tela do Player
                        from ui.screens.player import PlayerScreen
                        self.app.push_screen(PlayerScreen(server))
                        return # Sai da função com sucesso
                except (ValueError, IndexError):
                    self.notify("Erro ao identificar o servidor.", severity="error")
                    return

            # Se chegou aqui, nada foi selecionado ou o ID falhou
            self.notify("Selecione um servidor na lista primeiro!", severity="error")

        # Mantém as outras lógicas (logout, etc)
        elif event.button.id in ["add-server", "btn-logout"]:
            from ui.screens.login import LoginScreen
            self.app.push_screen(LoginScreen())