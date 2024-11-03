from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical


class ScreenApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Static("<<< MERGR 🍒")
        self.files = Static("")
        self.code = Static("")
        self.comment = Static("")
        self.command = Static("")


        with Vertical():
            yield self.widget


            with Horizontal():
                yield self.files   
                yield self.code
                yield self.comment

            yield self.command

    def on_mount(self) -> None:
        # Screen styles
        self.widget.styles.width = "100%"
        self.widget.styles.height = "auto"  # Adjust height to auto to fit content
        self.widget.styles.margin = 1
        self.widget.styles.text_align = "left"  # Ensure text is centered

        self.files.styles.border_left = ("dashed","#1C6FFF")
        self.files.styles.border_right = ("dashed","#1C6FFF")
        self.files.styles.border_top = ("double","#1C6FFF")
        self.files.styles.border_bottom = ("double","#1C6FFF")
        self.files.border_title = "FILES"
        self.files.border_title_align = "left"
        self.files.styles.border_title_color = "white"
        self.files.styles.height= "80vh"
        self.files.styles.width= "17vw"
        self.files.styles.margin = 3
        
        self.code.styles.border_left = ("dashed","#1C6FFF")
        self.code.styles.border_right = ("dashed","#1C6FFF")
        self.code.styles.border_top = ("double","#1C6FFF")
        self.code.styles.border_bottom = ("double","#1C6FFF")
        self.code.border_title = "CODE"
        self.code.border_title_align = "left"
        self.code.styles.border_title_color = "white"
        self.code.styles.height= "50vh"
        self.code.styles.width= "37vw"
        self.code.styles.margin = 3
        
        self.comment.styles.border_left = ("dashed","#1C6FFF")
        self.comment.styles.border_right = ("dashed","#1C6FFF")
        self.comment.styles.border_top = ("double","#1C6FFF")
        self.comment.styles.border_bottom = ("double","#1C6FFF")
        self.comment.border_title = "COMMENTS"
        self.comment.border_title_align = "left"
        self.comment.styles.border_title_color = "white"
        self.comment.styles.height= "50vh"
        self.comment.styles.width= "37vw"
        self.comment.styles.margin = 3

        self.command.styles.border_left = ("dashed","#1C6FFF")
        self.command.styles.border_right = ("dashed","#1C6FFF")
        self.command.styles.border_top = ("double","#1C6FFF")
        self.command.styles.border_bottom = ("double","#1C6FFF")
        self.command.border_title = "COMMAND"
        self.command.border_title_align = "left"
        self.command.styles.border_title_color = "white"
        self.command.styles.height= "10vh"
        self.command.styles.width= "74vw"
        self.command.styles.margin = 3

if __name__ == "__main__":
    app = ScreenApp()
    app.run()
