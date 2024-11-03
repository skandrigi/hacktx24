class StagingManager:
    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def stage_file(self, file_path):
        """Stage a file after resolving conflicts."""
        self.repo_manager.repo.index.add([file_path])

    def commit_resolution(self, message="Resolved merge conflicts"):
        """Commit the changes after resolving conflicts."""
        try:
            self.repo_manager.repo.git.commit(m=message)
        except Exception as e:
            print("Error while committing:", e)

    def continue_merge(self):
        """Finalize the merge process if all conflicts are resolved."""
        if not self.repo_manager.repo.index.diff("HEAD"):
            self.commit_resolution()
            print("Merge completed successfully.")
        else:
            print("Some conflicts are still unresolved.")
