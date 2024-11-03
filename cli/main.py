from textual.app import App, ComposeResult
from textual.widgets import Static


class ScreenApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Static("<<< MERGR 🍒")
        self.files = Static("")

        yield self.widget
        yield self.files

    def on_mount(self) -> None:
        # Screen styles
        self.widget.styles.width = "100%"
        self.widget.styles.height = "auto"  # Adjust height to auto to fit content
        self.widget.styles.background = "red"
        self.widget.styles.margin = 1
        self.widget.styles.text_align = "left"  # Ensure text is centered

        self.files.styles.border_left = ("dashed","#1C6FFF")
        self.files.styles.border_right = ("dashed","#1C6FFF")
        self.files.styles.border_top = ("double","#1C6FFF")
        self.files.styles.border_bottom = ("double","#1C6FFF")
        self.files.border_title = "FILES"
        self.files.border_title_align = "center"
        self.files.styles.border_title_color = "white"
        self.files.styles.height= "90vh"
        self.files.styles.width= "20vw"

if __name__ == "__main__":
    app = ScreenApp()
    app.run()
