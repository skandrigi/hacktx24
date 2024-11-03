import asyncio
from textual import events

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'uv add httpx' ")

import aiofiles
from inference import extract_answer, get_completion

from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree, Button, TextArea
from textual.containers import Horizontal, Vertical, ScrollableContainer
from rich.text import Text
from backend.repository import RepositoryManager
from backend.conflict import ConflictDetector
from backend.commit import CommitComparer
from backend.resolution import StagingManager

INITIAL_TEXT = 'Print("Hello World!")'

class ScreenApp(App):
    CSS_PATH = "boxes.tcss"
    position: int = 0
    def __init__(self, repo_path="./test_repo"):
        super().__init__()
        self.repo_manager = RepositoryManager(repo_path)
        self.conflict_detector = ConflictDetector(self.repo_manager)
        self.commit_comparer = CommitComparer(self.repo_manager)
        self.staging_manager = StagingManager(self.repo_manager)
        self.path = "."

    def compose(self) -> ComposeResult:
        self.widget = Static("<<< MERGR 🍒", id="header-widget")
        self.files = DirectoryTree("./", id="file-browser", classes="grid")
        self.code = TextArea.code_editor(INITIAL_TEXT, language="python", read_only=True, id="code-view", classes="grid")
        self.comment = Static("", id="comment-view", classes="grid")
        self.command = Static("", id="command-view", classes="grid")
        self.popup = Static("This is a temporary pop-up!", id="popup", classes="popup")

        yield self.widget
        yield self.files
        yield ScrollableContainer((self.code))
        yield self.comment
        yield self.popup

        with Horizontal(id="button-container"):
             yield Button("[a] Accept Incoming", id="resolve-button", classes="action-button")
             yield Button("[c] Accept Current", id="acceptcurr-button", classes="action-button")
             yield Button("[b] Accept Both", id="acceptboth-button", classes="action-button")

    def on_mount(self) -> None:
        # Set up initial view titles and styles
        files_title = Text("", style="white")
        files_title.append("FILES", style="white")
        self.files.border_title = files_title
        self.files.border_title_align = "left"

        code_title = Text("", style="white")
        code_title.append("C", style="white")
        code_title.append("\U00002b24", style="#FFABAB")
        code_title.append("DE", style="white")
        self.code.border_title = code_title
        self.code.border_title_align = "left"
        
        # Title for Comment View
        comment_title = Text("", style="white")
        comment_title.append("C", style="white")
        comment_title.append("\U00002b24", style="#FFABAB")
        comment_title.append("MMENTS", style="white")
        self.comment.border_title = comment_title
        self.comment.border_title_align = "left"

    async def on_key(self, event: events.Key) -> None:
        line = self.conflict_detector.get_conflict_lines(self, self.path)

        if event.key == "a":
            self.staging_manager.accept_incoming(self, self.path)
        elif event.key == "c":
            self.staging_manager.accept_current(self, self.path)
        elif event.key == "b":
            self.staging_manager.keep_both(self, self.path)
            

    async def define_commits(self, file_content, path):
        print("directory tree path:", self.query_one(DirectoryTree).path, "input path:",  path)
        # Use asynchronous file reading
        completion = await get_completion(file_content)
        answers = extract_answer(completion)

        if path == self.path:
            comment_view = self.query_one("#comment-view", Static)
            comment_view.update("".join(answers))

    async def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle the event when a file is selected in the directory tree."""
        event.stop()
        file_path = str(event.path)
        self.path = file_path
        
        # Do the quick file reading first
        with open(file_path, "r") as file:
            content = file.read()
        
        # Update UI immediately with file content
        code_view = self.query_one("#code-view")
        code_view.text = content
        comment_view = self.query_one("#comment-view", Static)
        # Run define_commits asynchronously to avoid blocking
        try:
            # Check for conflict markers and display conflicts
            if "<<<<<<<" in content and "=======" in content and ">>>>>>>" in content:
                conflict_sections = self.conflict_detector.parse_conflict_sections(
                    file_path
                )
                conflict_text = "\n".join(
                    f"--- Conflict Section {i+1} ---\nCurrent changes:\n{''.join(section['current'])}\nIncoming changes:\n{''.join(section['incoming'])}"
                    for i, section in enumerate(conflict_sections)
                )

                comment_view.update(conflict_text)


                # Display raw file content with conflict markers in the code view
                code_view.text = content

                # Provide resolution instructions to the user
                resolution_instruction = Text(
                    "Choose [c] to accept Current changes or [i] for Incoming changes.\n"
                )
                comment_view.update(resolution_instruction)
                asyncio.create_task(self.define_commits(content, file_path))

            else:
                # If no conflict markers are detected, display file content normally
                code_view.text = content
                comment_view.update("No conflicts detected in this file.")

        except Exception as e:
            # Handle errors in file loading
            code_view.text = "print('uh-oh')"
            comment_view.update(f"Error loading file: {e}")

    def resolve_conflict(self, file_path, choice="incoming"):
        """Resolve conflicts in the selected file based on user choice."""
        conflict_sections = self.conflict_detector.parse_conflict_sections(file_path)
        with open(file_path, "r") as f:
            lines = f.readlines()

        for section in conflict_sections:
            start, divider, end = section["start"], section["divider"], section["end"]
            # Apply the chosen resolution (current or incoming changes)
            if choice == "incoming":
                lines[start : end + 1] = section["incoming"]
            else:
                lines[start : end + 1] = section["current"]

        # Write resolved changes back to the file
        with open(file_path, "w") as f:
            f.writelines(lines)

        # Stage the resolved file for commit
        self.staging_manager.stage_file(file_path)
        self.comment.update(f"{file_path} staged with {choice} resolution.")

    def finalize_merge(self):
        """Finalize the merge process if all conflicts are resolved."""
        if not self.repo_manager.get_files_status():
            self.staging_manager.continue_merge()
            self.comment.update("Merge completed successfully.")
            self.show_temp_popup("Conflicts detected!")
        else:
            self.comment.update(
                "Some conflicts are still unresolved. Resolve all conflicts to complete the merge."
            )


if __name__ == "__main__":
    repo_path = "./test_repo"  # Specify path to your repository
    app = ScreenApp()
    app.run()
