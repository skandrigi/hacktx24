from textual.app import App, ComposeResult
from textual.widgets import Static

class ScreenApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Static("<<< MERGR 🍒")
        self.files = Static("FILES")

        yield self.widget
        yield self.files

    def on_mount(self) -> None:
        # Screen styles
        self.screen.styles.background = "#161b2a"
        self.widget.styles.width = "3fr"
        self.widget.styles.min_height = "10vh"
        self.widget.styles.background = "red"
        self.widget.styles.padding = 2
        self.files.styles.border_left = ("dashed","#1C6FFF")
        self.files.styles.border_right = ("dashed","#1C6FFF")
        self.files.styles.border_top = ("double","#1C6FFF")
        self.files.styles.border_bottom = ("double","#1C6FFF")
        self.files.styles.border_title = "FILES"
        self.files.styles.min_height= "90vh"
        self.files.styles.min_width= "20vh"

if __name__ == "__main__":
    app = ScreenApp()
    app.run()
