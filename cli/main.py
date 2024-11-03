import asyncio

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

from backend.merge_conflict_manager import MergeConflictManager
from backend.conflict import ConflictDetector
from backend.resolution import StagingManager
from cli.backend.main import MergeConflictCLI
# from backend.openai import OpenAIClient

INITIAL_TEXT = 'Print("Hello World!")'

class ScreenApp(App):
    CSS_PATH = "boxes.tcss"
    position: int = 0

    def __init__(self, openai_api_key):
        # Backend initialization
        self.conflict_manager = MergeConflictManager(conflicts_folder="cli/merge-conflicts")
        self.conflict_detector = ConflictDetector()
        self.staging_manager = StagingManager()
        # self.openai_client = OpenAIClient(openai_api_key)

    def handle_conflicts(self):
        """Load conflict files, detect conflicts, and guide user through resolution."""
        conflict_files = self.conflict_manager.load_conflict_files()

        for filename, lines in conflict_files.items():
            print(f"\nHandling conflicts in {filename}")
            conflicts = self.conflict_detector.parse_conflict_sections(lines)

            for conflict in conflicts:
                current = "".join(conflict["current"])
                incoming = "".join(conflict["incoming"])

                print("\nCurrent changes:\n", current)
                print("\nIncoming changes:\n", incoming)

                suggestion = self.openai_client.get_suggestion(current, incoming)
                print("\nAI Suggested resolution:\n", suggestion)

                choice = input("Choose resolution ([c] Current, [i] Incoming, [a] AI Suggested, [b] Both): ")
                if choice == "c":
                    self.staging_manager.resolve_conflict(conflict, "current")
                elif choice == "i":
                    self.staging_manager.resolve_conflict(conflict, "incoming")
                elif choice == "a":
                    self.staging_manager.resolve_conflict(conflict, suggestion)
                elif choice == "b":
                    self.staging_manager.resolve_conflict(conflict, "both")
                else:
                    print("Invalid choice, defaulting to Incoming")
                    self.staging_manager.resolve_conflict(conflict, "incoming")

            # Save the resolved content for each file after all conflicts in the file are resolved
            self.staging_manager.save_resolved_content(filename)

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

        # with Horizontal(id="button-container"):
        #     yield Button("\U000015E3 Accept Incoming", id="resolve-button", classes="action-button")
        #     yield Button("🍊 Accept Current", id="acceptcurr-button", classes="action-button")
        #     yield Button("🍓 Accept Both", id="acceptboth-button", classes="action-button")
        #     yield Button("🤖 Accept AI", id="ai-button", classes="action-button")

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
        
        with open(file_path, "r") as file:
            content = file.read()
        
        code_view = self.query_one("#code-view")
        code_view.text = content
        comment_view = self.query_one("#comment-view", Static)
        
        try:
            if "<<<<<<<" in content and "=======" in content and ">>>>>>>" in content:
                conflict_sections = self.conflict_detector.parse_conflict_sections(content.splitlines())
                conflict_text = "\n".join(
                    f"--- Conflict Section {i+1} ---\nCurrent changes:\n{''.join(section['current'])}\nIncoming changes:\n{''.join(section['incoming'])}"
                    for i, section in enumerate(conflict_sections)
                )

                comment_view.update(conflict_text)
                code_view.text = content
                resolution_instruction = Text(
                    "Choose [c] to accept Current changes, [i] for Incoming changes, [a] for AI Suggested, or [b] for Both.\n"
                )
                comment_view.update(resolution_instruction)

            else:
                code_view.text = content
                comment_view.update("No conflicts detected in this file.")

        except Exception as e:
            code_view.text = "print('uh-oh')"
            comment_view.update(f"Error loading file: {e}")

    # Use backend functions

    # def resolve_conflict(self, file_path, choice="incoming"):
    #     """Resolve conflicts in the selected file based on user choice."""
    #     conflict_sections = self.conflict_detector.parse_conflict_sections(file_path)
    #     with open(file_path, "r") as f:
    #         lines = f.readlines()

    #     for section in conflict_sections:
    #         start, divider, end = section["start"], section["divider"], section["end"]
    #         # Apply the chosen resolution (current or incoming changes)
    #         if choice == "incoming":
    #             lines[start : end + 1] = section["incoming"]
    #         else:
    #             lines[start : end + 1] = section["current"]

    #     # Write resolved changes back to the file
    #     with open(file_path, "w") as f:
    #         f.writelines(lines)

    #     # Stage the resolved file for commit
    #     self.staging_manager.stage_file(file_path)
    #     self.comment.update(f"{file_path} staged with {choice} resolution.")

    # def finalize_merge(self):
    #     """Finalize the merge process if all conflicts are resolved."""
    #     if not self.repo_manager.get_files_status():
    #         self.staging_manager.continue_merge()
    #         self.comment.update("Merge completed successfully.")
    #         self.show_temp_popup("Conflicts detected!")
    #     else:
    #         self.comment.update(
    #             "Some conflicts are still unresolved. Resolve all conflicts to complete the merge."
    #         )

if __name__ == "__main__":
    tool = MergeConflictCLI(openai_api_key="your_openai_api_key_here")
    tool.handle_conflicts()
    app = ScreenApp()
    app.run()
