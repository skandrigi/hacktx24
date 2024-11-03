from textual.app import App, ComposeResult
from textual.widgets import Static

class ScreenApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Static("hi")
        self.gir = Static("hi1")
        
        yield self.widget
        yield self.gir

    def on_mount(self) -> None:
        # Screen styles
        self.screen.styles.background = "#161b2a"
        self.screen.styles.border = ("heavy", "white")
        self.widget.styles.width = "2fr"
        self.widget.styles.height = "3fr"
        self.widget.styles.background = "red"
        self.gir.styles.width = "1fr"
        self.gir.styles.height = "3fr"
        self.gir.styles.background = "purple"

if __name__ == "__main__":
    app = ScreenApp()
    app.run()
