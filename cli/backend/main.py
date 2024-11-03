from cli.backend.openai import OpenAIClient
from repository import RepositoryManager
from conflict import ConflictDetector
from commit import CommitComparer
from resolution import StagingManager

class MergeConflictTool:
    def __init__(self, repo_path, openai_api_key):
        self.repo_manager = RepositoryManager(repo_path)
        self.conflict_detector = ConflictDetector(self.repo_manager)
        self.commit_comparer = CommitComparer(self.repo_manager)
        self.staging_manager = StagingManager(self.repo_manager)
        self.openai_client = OpenAIClient(openai_api_key)  # Use OpenAIClient here

    def handle_merge_conflict(self):
        conflicts = self.conflict_detector.detect_conflicts()
        if conflicts:
            for file in conflicts:
                print(f"Conflict in {file}")
                conflict_sections = self.conflict_detector.parse_conflict_sections(file)
                for section in conflict_sections:
                    current_changes = "".join(section["current"])
                    incoming_changes = "".join(section["incoming"])
                    
                    print("Current changes:\n", current_changes)
                    print("Incoming changes:\n", incoming_changes)
                    
                    # Use OpenAI client to get a suggested resolution
                    suggestion = self.openai_client.get_suggestion(current_changes, incoming_changes)
                    print("AI Suggested resolution:\n", suggestion)
                    
                    # Prompt the user to choose a resolution
                    user_choice = input("Choose resolution ([1] Current, [2] Incoming, [3] AI Suggested): ")
                    if user_choice == "1":
                        resolved_content = current_changes
                    elif user_choice == "2":
                        resolved_content = incoming_changes
                    elif user_choice == "3":
                        resolved_content = suggestion
                    else:
                        print("Invalid choice, defaulting to incoming changes.")
                        resolved_content = incoming_changes

                    # Save the resolved content to the file
                    with open(file, "w") as f:
                        f.write(resolved_content)

                    # Stage the file after resolution
                    self.staging_manager.stage_file(file)

            # Continue the merge after all conflicts are resolved
            self.staging_manager.continue_merge()
        else:
            print("No merge conflicts detected.")

# Instantiate and run with OpenAI API key
tool = MergeConflictTool("/path/to/repo", openai_api_key="tamuhack")
tool.handle_merge_conflict()
