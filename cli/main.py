from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree
from textual.containers import Horizontal, Vertical
from rich.traceback import Traceback
from rich.syntax import Syntax
from rich.text import Text


class ScreenApp(App):
    CSS_PATH = "boxes.tcss"
    def compose(self) -> ComposeResult:
        self.widget = Static("<<< MERGR 🍒", id="header-widget")
        self.files = DirectoryTree("./", id="file-browser", classes="grid")
        self.code = Static("", id="code-view", classes="grid")
        self.comment = Static("", id="comment-view", classes="grid")
        self.command = Static("", id="command-view", classes="grid")

        yield self.widget
        yield self.files
        yield self.code
        yield self.comment

    def on_mount(self) -> None:
        # Screen styles
        self.screen.styles.background = "#2B263B"
        self.widget.styles.width = "100%"
        self.widget.styles.height = "auto"  # Adjust height to auto to fit content
        self.widget.styles.margin = 2
        self.widget.styles.text_align = "left"  # Ensure text is centered

        self.files.styles.background = "#2B263B"
        self.files.styles.border_left = ("dashed","#1C6FFF")
        self.files.styles.border_right = ("dashed","#1C6FFF")
        self.files.styles.border_top = ("double","#1C6FFF")
        self.files.styles.border_bottom = ("double","#1C6FFF")
        self.files.border_title = "FILES"
        self.files.border_title_align = "left"
        self.files.styles.border_title_color = "white"
        self.files.styles.height= "76vh"
        self.files.styles.width= "17vw"
        self.files.styles.margin = 2
        
        code_title = Text("C", style="white")
        code_title.append("\U00002B24", style="FFABAB") 
        code_title.append("DE", style="white")
        
        self.code.styles.background = "#2B263B"
        self.code.styles.border_left = ("dashed","#1C6FFF")
        self.code.styles.border_right = ("dashed","#1C6FFF")
        self.code.styles.border_top = ("double","#1C6FFF")
        self.code.styles.border_bottom = ("double","#1C6FFF")
        self.code.border_title = code_title
        self.code.border_title_align = "left"
        self.code.styles.border_title_color = "white"
        self.code.styles.height= "76vh"
        self.code.styles.width= "37vw"
        self.code.styles.margin = 2

        comment_title = Text("C", style="white")
        comment_title.append("\U00002B24", style="FFABAB") 
        comment_title.append("\U000015E3", style="FFABAB") 
        comment_title.append("MMENTS", style="white")
        self.code.styles.overflow = "auto" 
        
        self.comment.styles.border_left = ("dashed","#1C6FFF")
        self.comment.styles.border_right = ("dashed","#1C6FFF")
        self.comment.styles.border_top = ("double","#1C6FFF")
        self.comment.styles.border_bottom = ("double","#1C6FFF")
        self.comment.border_title = comment_title
        self.comment.border_title_align = "left"
        self.comment.styles.border_title_color = "white"
        self.comment.styles.height= "76vh"
        self.comment.styles.width= "37vw"
        self.comment.styles.margin = 2

        command_title = Text("C", style="white")
        command_title.append("\U00002B24", style="FFABAB") 
        command_title.append("MMAND", style="white")

        self.command.styles.border_left = ("dashed","#1C6FFF")
        self.command.styles.border_right = ("dashed","#1C6FFF")
        self.command.styles.border_top = ("double","#1C6FFF")
        self.command.styles.border_bottom = ("double","#1C6FFF")
        self.command.border_title = command_title 
        self.command.border_title_align = "left"
        self.command.styles.border_title_color = "white"
        self.command.styles.height= "13vh"
        self.command.styles.width= "75vw"
        self.command.styles.margin = 2
        self.comment.styles.overflow = "auto" 

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        event.stop()
        code_view = self.query_one("#code-view", Static)

        try:
            syntax = Syntax.from_path(
                str(event.path),
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark"
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
        else:
            code_view.update(syntax)

if __name__ == "__main__":
    app = ScreenApp()
    app.run()