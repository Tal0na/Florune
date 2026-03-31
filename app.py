from textual.app import App
from ui.screens.login import LoginScreen
from ui.screens.dashboard import Dashboard
from core.config import ConfigManager

class Florune(App):
    def on_mount(self) -> None:
        self.cfg = ConfigManager()
        
        # Se já tem servidor salvo, pula o login e vai pro Dashboard
        if self.cfg.has_servers():
            self.push_screen(Dashboard())
        else:
            self.push_screen(LoginScreen())

if __name__ == "__main__":
    Florune().run()