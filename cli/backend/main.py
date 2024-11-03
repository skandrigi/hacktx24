from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree, Button
from textual.containers import Horizontal, Vertical
from rich.traceback import Traceback
from rich.syntax import Syntax
from rich.text import Text
from backend.repository import RepositoryManager
from backend.conflict import ConflictDetector
from backend.commit import CommitComparer
from backend.resolution import StagingManager
from resolution import accept_incoming, accept_current, keep_both

def handle_merge_conflict(self):
    conflicts = self.conflict_detector.detect_conflicts()
    if conflicts:
        for file in conflicts:
            print(f"Conflict in {file}")
            conflict_sections = self.conflict_detector.parse_conflict_sections(file)
            for section in conflict_sections:
                print("Current changes:\n", "".join(section["current"]))
                print("Incoming changes:\n", "".join(section["incoming"]))

            # AI-based suggestion placeholder
            print("Suggested resolution: Choose the incoming changes.")

            # Stage the file after resolution
            self.staging_manager.stage_file(file)

        self.staging_manager.continue_merge()
    else:
        print("No merge conflicts detected.")
        
class ScreenApp(App):
    CSS_PATH = "boxes.tcss"

    def __init__(self, repo_path="./test_repo"):
        super().__init__()
        self.repo_manager = RepositoryManager(repo_path)
        self.conflict_detector = ConflictDetector(self.repo_manager)
        self.commit_comparer = CommitComparer(self.repo_manager)
        self.staging_manager = StagingManager(self.repo_manager)
        self.current_file = None  # Store the current file path

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

        with Horizontal(id="button-container"):
            yield Button("\U000015E3 Accept Incoming", id="resolve-button", classes="action-button", on_click=self.on_accept_incoming)
            yield Button("🍊 Accept Current", id="acceptcurr-button", classes="action-button", on_click=self.on_accept_current)
            yield Button("🍓 Keep Both", id="acceptboth-button", classes="action-button", on_click=self.on_keep_both)
            yield Button("🤖 Use AI", id="ai-button", classes="action-button", on_click=self.on_handle_merge_conflict)

    def on_mount(self) -> None:
        # Set up initial view titles and styles
        self.files.styles.background = "#2B263B"
        self.code.border_title = "CODE VIEW"
        self.comment.border_title = "COMMENTS"
        self.command.border_title = "COMMANDS"

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle the event when a file is selected in the directory tree."""
        event.stop()
        self.current_file = str(event.path)
        code_view = self.query_one("#code-view", Static)
        comment_view = self.query_one("#comment-view", Static)

        try:
            # Read the selected file's content
            with open(self.current_file, "r") as file:
                content = file.read()

            # Check for conflict markers and display conflicts
            if "<<<<<<<" in content and "=======" in content and ">>>>>>>" in content:
                conflict_sections = self.conflict_detector.parse_conflict_sections(self.current_file)
                conflict_text = "\n".join(
                    f"--- Conflict Section {i+1} ---\nCurrent changes:\n{''.join(section['current'])}\nIncoming changes:\n{''.join(section['incoming'])}"
                    for i, section in enumerate(conflict_sections)
                )
                comment_view.update(conflict_text)

                # Display raw file content with conflict markers in the code view
                syntax = Syntax(content, "text", line_numbers=True, theme="github-dark")
                code_view.update(syntax)

                # Provide resolution instructions to the user
                resolution_instruction = Text("Choose [c] to accept Current changes or [i] for Incoming changes.\n")
                comment_view.update(resolution_instruction)
            else:
                # If no conflict markers are detected, display file content normally
                syntax = Syntax(content, "text", line_numbers=True, theme="github-dark")
                code_view.update(syntax)
                comment_view.update("No conflicts detected in this file.")

        except Exception as e:
            # Handle errors in file loading
            code_view.update(Traceback(theme="github-dark"))
            comment_view.update(f"Error loading file: {e}")

    # Button handlers calling imported functions
    def on_accept_incoming(self) -> None:
        if self.current_file:
            accept_incoming(self, self.current_file)

    def on_accept_current(self) -> None:
        if self.current_file:
            accept_current(self, self.current_file)

    def on_keep_both(self) -> None:
        if self.current_file:
            keep_both(self, self.current_file)

    def on_handle_merge_conflict(self) -> None:
        handle_merge_conflict(self)

if __name__ == "__main__":
    repo_path = "./test_repo"  # Specify path to your repository
    app = ScreenApp()
    app.run()
