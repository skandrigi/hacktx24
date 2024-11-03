from backend.merge_conflict_manager import MergeConflictManager
from backend.conflict import ConflictDetector
from backend.resolution import StagingManager
from backend.openai import OpenAIClient

class MergeConflictCLI:
    def __init__(self, openai_api_key):
        self.conflict_manager = MergeConflictManager()
        self.conflict_detector = ConflictDetector()
        self.staging_manager = StagingManager()
        self.openai_client = OpenAIClient(openai_api_key)

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

                # Fetch AI suggestion
                suggestion = self.openai_client.get_suggestion(current, incoming)
                print("\nAI Suggested resolution:\n", suggestion)

                # User choice
                choice = input("Choose resolution ([1] Current, [2] Incoming, [3] AI Suggested, [4] Both): ")
                if choice == "1":
                    self.staging_manager.resolve_conflict(conflict, "current")
                elif choice == "2":
                    self.staging_manager.resolve_conflict(conflict, "incoming")
                elif choice == "3":
                    self.staging_manager.resolve_conflict(conflict, suggestion)
                elif choice == "4":
                    self.staging_manager.resolve_conflict(conflict, "both")
                else:
                    print("Invalid choice, defaulting to Incoming")
                    self.staging_manager.resolve_conflict(conflict, "incoming")

            # Save the resolved content for each file
            self.staging_manager.save_resolved_content(filename)

# Run the CLI
if __name__ == "__main__":
    tool = MergeConflictCLI(openai_api_key="your_openai_api_key_here")
    tool.handle_conflicts()
