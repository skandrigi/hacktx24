from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree
from textual.containers import Horizontal, Vertical
from rich.traceback import Traceback
from rich.syntax import Syntax
from rich.text import Text
from backend.repository import RepositoryManager
from backend.conflict import ConflictDetector
from backend.commit import CommitComparer
from backend.resolution import StagingManager


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
        self.screen.styles.background = "#28233B"
        self.widget.styles.width = "100%"
        self.widget.styles.height = "auto"  # Adjust height to auto to fit content
        self.widget.styles.margin = 2
        self.widget.styles.text_align = "left"  # Ensure text is centered

        self.files.styles.background = "#28233B"
        self.files.styles.border_left = ("dashed", "#1C6FFF")
        self.files.styles.border_right = ("dashed", "#1C6FFF")
        self.files.styles.border_top = ("double", "#1C6FFF")
        self.files.styles.border_bottom = ("double", "#1C6FFF")
        self.files.border_title = "FILES"
        self.files.border_title_align = "left"
        self.files.styles.border_title_color = "white"
        self.files.styles.height = "76vh"
        self.files.styles.width = "17vw"
        self.files.styles.margin = 2

        code_title = Text("", style="white")
        code_title.append("C", style="white")
        code_title.append("\U00002b24", style="#FFABAB")
        code_title.append("DE", style="white")

        self.code.styles.background = "#28233B"
        self.code.styles.border_left = ("dashed", "#1C6FFF")
        self.code.styles.border_right = ("dashed", "#1C6FFF")
        self.code.styles.border_top = ("double", "#1C6FFF")
        self.code.styles.border_bottom = ("double", "#1C6FFF")
        self.code.border_title = code_title
        self.code.border_title_align = "left"
        self.code.styles.height = "76vh"
        self.code.styles.width = "37vw"
        self.code.styles.margin = 2

        comment_title = Text("C", style="white")
        comment_title.append("\U00002b24", style="#FFABAB")
        comment_title.append("MMENTS", style="white")
        self.code.styles.overflow = "auto"

        self.comment.styles.border_left = ("dashed", "#1C6FFF")
        self.comment.styles.border_right = ("dashed", "#1C6FFF")
        self.comment.styles.border_top = ("double", "#1C6FFF")
        self.comment.styles.border_bottom = ("double", "#1C6FFF")
        self.comment.border_title = comment_title
        self.comment.border_title_align = "left"
        self.comment.styles.border_title_color = "white"
        self.comment.styles.height = "76vh"
        self.comment.styles.width = "37vw"
        self.comment.styles.margin = 2

        command_title = Text("C", style="white")
        command_title.append("\U00002b24", style="#FFABAB")
        command_title.append("MMAND", style="white")

        self.command.styles.border_left = ("dashed", "#1C6FFF")
        self.command.styles.border_right = ("dashed", "#1C6FFF")
        self.command.styles.border_top = ("double", "#1C6FFF")
        self.command.styles.border_bottom = ("double", "#1C6FFF")
        self.command.border_title = command_title
        self.command.border_title_align = "left"
        self.command.styles.height = "13vh"
        self.command.styles.width = "75vw"
        self.command.styles.margin = 2
        self.comment.styles.overflow = "auto"

    # test_repo < example.txt has merge conflicts < when example.txt selected in cli = No conflicts detected in this file.
    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        event.stop()
        code_view = self.query_one("#code-view", Static)
        comment_view = self.query_one("#comment", Static)

        # Get the path of the selected file
        file_path = str(event.path)

        # Read the file content and check for conflict markers
        try:
            with open(file_path, "r") as file:
                content = file.read()

            # Look for conflict markers directly in the file content
            if "<<<<<<<" in content and "=======" in content and ">>>>>>>" in content:
                # If conflict markers are found, parse the conflicting sections
                conflict_sections = self.conflict_detector.parse_conflict_sections(
                    file_path
                )
                conflict_text = ""
                for i, section in enumerate(conflict_sections):
                    conflict_text += f"\n--- Conflict Section {i+1} ---\n"
                    conflict_text += (
                        f"Current changes:\n{''.join(section['current'])}\n"
                    )
                    conflict_text += (
                        f"Incoming changes:\n{''.join(section['incoming'])}\n"
                    )

                # Update the comments view with parsed conflict details
                comment_view.update(conflict_text)

                # Display the raw file content (including conflict markers) in the code view
                syntax = Syntax(
                    content,
                    "text",
                    line_numbers=True,
                    word_wrap=False,
                    theme="github-dark",
                )
                code_view.update(syntax)
            else:
                # If no conflict markers are found, display file content normally
                syntax = Syntax(
                    content,
                    "text",
                    line_numbers=True,
                    word_wrap=False,
                    theme="github-dark",
                )
                code_view.update(syntax)
                comment_view.update("No conflicts detected in this file.")

        except Exception as e:
            # Handle errors and show traceback if file loading fails
            code_view.update(Traceback(theme="github-dark", width=None))
            comment_view.update(f"Error: {e}")


if __name__ == "__main__":
    repo_path = "./test_repo"  # local path to a mock repository
    app = ScreenApp()
    app.run()
