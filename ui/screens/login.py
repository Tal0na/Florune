import json
import os
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Button, Select, Label, ListView, ListItem, Header, Footer
from textual.widgets.select import NoSelection
from textual.containers import Vertical
from core.config import ConfigManager

class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="login-panel"):
            yield Label("[b]FLORUNE: ACESSAR[/b]")

            # 1. Lista de contas salvas (Só aparece se houver algo no config.json)
            self.config = ConfigManager()
            if self.config.has_servers():
                yield Label("Escolha uma conta salva:")
                yield ListView(id="saved-accounts")
                yield Label("[dim]— ou cadastre uma nova —[/dim]", id="divider")

            # 2. Formulário de Novo Login
            yield Select([("jelly", "Jellyfin"), ("navi", "Navidrome")], prompt="Tipo", id="server-type")
            yield Input(placeholder="URL do Servidor", id="url")
            yield Input(placeholder="Usuário", id="user")
            yield Input(placeholder="Senha", password=True, id="password")
            yield Button("ENTRAR", variant="success", id="login-btn")
        yield Footer()

    def on_mount(self) -> None:
        """Popula a lista de contas se existirem."""
        if self.config.has_servers():
            lista = self.query_one("#saved-accounts", ListView)
            for i, s in enumerate(self.config.get_all_active()):
                lista.mount(ListItem(Label(f"👤 {s['user']} @ {s['name']}"), id=f"old-{i}"))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Entra direto ao selecionar uma conta da lista."""
        if event.item and event.item.id and event.item.id.startswith("old-"):
            from ui.screens.dashboard import Dashboard
            self.app.push_screen(Dashboard())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login-btn":
            tipo = self.query_one("#server-type", Select).value
            url = self.query_one("#url", Input).value
            user = self.query_one("#user", Input).value
            pw = self.query_one("#password", Input).value

            if isinstance(tipo, NoSelection) or not all([url, user, pw]):
                self.notify("Preencha todos os campos!", severity="error")
                return

            novo_server = {
                "name": f"Meu {str(tipo).capitalize()}",
                "type": str(tipo),
                "url": url,
                "user": user,
                "password": pw
            }

            self.salvar_no_config(novo_server)
            from ui.screens.dashboard import Dashboard
            self.app.push_screen(Dashboard())

    def salvar_no_config(self, novo_server):
        config_path = "config.json"
        dados = {"servers": [], "active_server_id": 0}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                dados = json.load(f)
        dados["servers"].append(novo_server)
        dados["active_server_id"] = len(dados["servers"]) - 1
        with open(config_path, "w") as f:
            json.dump(dados, f, indent=4)