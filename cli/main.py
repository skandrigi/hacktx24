import asyncio

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'uv add httpx' ")

import aiofiles
from inference import extract_answer, get_completion

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


class ScreenApp(App):
    CSS_PATH = "boxes.tcss"

    def __init__(self, repo_path="./test_repo"):
        super().__init__()
        self.repo_manager = RepositoryManager(repo_path)
        self.conflict_detector = ConflictDetector(self.repo_manager)
        self.commit_comparer = CommitComparer(self.repo_manager)
        self.staging_manager = StagingManager(self.repo_manager)

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
            yield Button("🍊 Commit", id="commit-button", classes="action-button")
            yield Button("\U000025aa Stage", id="stage-button", classes="action-button")
            yield Button(
                "\U000015e3 Resolve", id="resolve-button", classes="action-button"
            )

    def on_mount(self) -> None:
        # Set up initial view titles and styles
        self.files.styles.background = "#2B263B"
        self.code.border_title = "CODE VIEW"
        self.comment.border_title = "COMMENTS"
        self.command.border_title = "COMMANDS"

    async def define_commits(self, file_content):
        print("in define_commits")
        # Use asynchronous file reading
        async with aiofiles.open(file_content, 'r') as f:
            content = await f.read()
            completion = await get_completion(content)
            print(completion)
            # answers = extract_answer(completion)


        comment_view = self.query_one("#comment-view", Static)
        if file_content == self.query_one(DirectoryTree).path:
            comment_view.update("hello")

    async def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle the event when a file is selected in the directory tree."""
        event.stop()
        file_path = str(event.path)
        
        # Do the quick file reading first
        with open(file_path, "r") as file:
            content = file.read()
        
        # Update UI immediately with file content
        code_view = self.query_one("#code-view", Static)
        syntax = Syntax(content, "text", line_numbers=True, theme="github-dark")
        code_view.update(syntax)
        comment_view = self.query_one("#comment-view", Static)
        # Run define_commits asynchronously to avoid blocking
        # asyncio.create_task(self.define_commits(event.path))
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
                syntax = Syntax(content, "text", line_numbers=True, theme="github-dark")
                code_view.update(syntax)

                # Provide resolution instructions to the user
                resolution_instruction = Text(
                    "Choose [c] to accept Current changes or [i] for Incoming changes.\n"
                )
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
        else:
            self.comment.update(
                "Some conflicts are still unresolved. Resolve all conflicts to complete the merge."
            )


if __name__ == "__main__":
    repo_path = "./test_repo"  # Specify path to your repository
    app = ScreenApp()
    app.run()
