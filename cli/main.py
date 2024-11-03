import asyncio
from textual import events

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'uv add httpx'")

import aiofiles
from inference import extract_answer, get_completion
from collections import deque
from textual.reactive import reactive
from textual.widget import Widget
from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree, Button, TextArea, Selection
from textual.containers import Horizontal, Vertical, ScrollableContainer
from rich.style import Style
from rich.text import Text
from textual.widgets.text_area import TextAreaTheme

from backend.merge_conflict_manager import MergeConflictManager
from backend.conflict import ConflictDetector
from backend.resolution import StagingManager

INITIAL_TEXT = 'Print("Hello World!")'

class ScreenApp(App):
    CSS_PATH = "boxes.tcss"
    comment_content = reactive("This is the initial content")
    merge_queue = reactive(deque(list(ConflictDetector.conflict_manager.parse_conflict_sections())))

    def __init__(self, openai_api_key=None):
        # Backend initialization
        super().__init__()
        self.conflict_manager = MergeConflictManager(conflicts_folder="cli/merge-conflicts")
        self.conflict_detector = ConflictDetector()
        self.staging_manager = StagingManager()
        # Optionally, initialize OpenAI client here if needed for AI conflict resolution
        # self.openai_client = OpenAIClient(openai_api_key) if openai_api_key else None
    
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

                # Optional: Use AI suggestion if OpenAI client is initialized
                suggestion = self.openai_client.get_suggestion(current, incoming) if self.openai_client else None
                if suggestion:
                    print("\nAI Suggested resolution:\n", suggestion)

                # User choice
                choice = input("Choose resolution ([c] Current, [i] Incoming, [a] AI Suggested, [b] Both): ")
                if choice == "c":
                    self.staging_manager.resolve_conflict(conflict, "current")
                elif choice == "i":
                    self.staging_manager.resolve_conflict(conflict, "incoming")
                elif choice == "a" and suggestion:
                    self.staging_manager.resolve_conflict(conflict, suggestion)
                elif choice == "b":
                    self.staging_manager.resolve_conflict(conflict, "both")
                else:
                    print("Invalid choice, defaulting to Incoming")
                    self.staging_manager.resolve_conflict(conflict, "incoming")

            # Save resolved content for each file
            self.staging_manager.save_resolved_content(filename)

    def compose(self) -> ComposeResult:
        # Define UI components
        self.widget = Static("<<< MERGR 🍒", id="header-widget")
        self.files = DirectoryTree("./", id="file-browser", classes="grid")
        self.code = TextArea.code_editor(INITIAL_TEXT, language="python", read_only=True, id="code-view", classes="grid", theme="dracula")
        dracula = TextAreaTheme.get_builtin_theme("dracula")
        my_theme = TextAreaTheme(
            name="pacs",
            base_style=Style(bgcolor="#28233B"),
            cursor_style=Style(color="white", bgcolor="blue"),
            syntax_styles={
                **dracula.syntax_styles,
                "string": Style(color="#FFABAB"),
                "comment": Style(color="#FFD153"),
                "function": Style(color="#FFD153")
            }
        )
        self.code.register_theme(my_theme)
        self.code.theme = "pacs"
        self.comment = Static("", id="comment-view", classes="grid")
        self.popup = Static("This is a temporary pop-up!", id="popup", classes="popup")

        yield self.widget
        yield self.files
        yield ScrollableContainer((self.code))
        yield self.comment
        yield self.popup

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

    async def on_key(self, merge_queue, event: events.Key) -> None:
        """Handle keyboard input for conflict resolution actions."""
        if merge_queue:
            if event.key == "a":
                merge_queue.popleft()
                next_conflict = merge_queue[0]
                self.code.text_area.cursor_location = (next_conflict[0],0)
                self.code.text_area.selection = Selection(start=(next_conflict[0], 0), end=(next_conflict[1], 0))
                self.staging_manager.accept_incoming(self.path)
            elif event.key == "c":
                merge_queue.popleft()
                next_conflict = merge_queue[0]
                self.code.text_area.cursor_location = (next_conflict[0],0)
                self.code.text_area.selection = Selection(start=(next_conflict[0], 0), end=(next_conflict[1], 0))
                self.staging_manager.accept_current(self.path)
            elif event.key == "b":
                merge_queue.popleft()
                next_conflict = merge_queue[0]
                self.code.text_area.cursor_location = (next_conflict[0],0)
                self.code.text_area.selection = Selection(start=(next_conflict[0], 0), end=(next_conflict[1], 0))
                self.staging_manager.keep_both(self.path)

    async def define_commits(self, file_content, path):
        """Retrieve and display commit information asynchronously."""
        completion = await get_completion(file_content)
        answers = extract_answer(completion)
        if path == self.path:
            self.comment_content = "".join(answers)

    async def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Display selected file content and detect conflicts."""
        event.stop()
        file_path = str(event.path)
        self.path = file_path

        with open(file_path, "r") as file:
            content = file.read()

        code_view = self.query_one("#code-view")
        code_view.text = content

        try:
            if "<<<<<<<" in content and "=======" in content and ">>>>>>>" in content:
                conflict_sections = self.conflict_detector.parse_conflict_sections(content.splitlines())
                conflict_text = "\n".join(
                    f"--- Conflict Section {i+1} ---\nCurrent changes:\n{''.join(section['current'])}\nIncoming changes:\n{''.join(section['incoming'])}"
                    for i, section in enumerate(conflict_sections)
                )
                self.comment_content = conflict_text
            else:
                self.comment_content = "No conflicts detected in this file."
        except Exception as e:
            self.comment_content = f"Error loading file: {e}"

    def show_temp_popup(self, message):
        """Display a temporary popup with a message."""
        popup = self.query_one("#popup", Static)
        popup.update(message)
        popup.styles.display = "block" 
        self.set_timer(2, lambda: self.hide_temp_popup())

    def hide_temp_popup(self):
        """Hide the temporary popup."""
        popup = self.query_one("#popup", Static)
        popup.styles.display = "none"

if __name__ == "__main__":
    app = ScreenApp(openai_api_key="your_openai_api_key_here")
    app.run()
