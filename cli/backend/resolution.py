from git import Repo

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

    def accept_incoming(self, file_path):
        """Accept incoming changes from the merging branch."""
        with open(file_path, 'r') as file:
            content = file.readlines()

        # Assume incoming changes are marked with a specific marker like '>>>>>>>' 
        # and we are keeping only the incoming section
        incoming_changes = []
        skip = False
        for line in content:
            if line.startswith(">>>>>>"):
                skip = True  # Start of incoming changes
                continue
            elif line.startswith("<<<<<<"):
                skip = False  # End of incoming changes
                continue
            if skip:
                incoming_changes.append(line)

        # Write the incoming changes back to the file
        with open(file_path, 'w') as file:
            file.writelines(incoming_changes)

        self.stage_file(file_path)

    def accept_current(self, file_path):
        """Accept current changes from the current branch."""
        with open(file_path, 'r') as file:
            content = file.readlines()

        # Assume current changes are marked with a specific marker like '<<<<<<'
        current_changes = []
        skip = False
        for line in content:
            if line.startswith("<<<<<<"):
                skip = True  # Start of current changes
                continue
            elif line.startswith(">>>>>>"):
                skip = False  # End of current changes
                continue
            if not skip:
                current_changes.append(line)

        # Write the current changes back to the file
        with open(file_path, 'w') as file:
            file.writelines(current_changes)

        self.stage_file(file_path)

    def keep_both(self, file_path):
        """Keep both changes and separate them with markers."""
        with open(file_path, 'r') as file:
            content = file.readlines()

        incoming_changes = []
        current_changes = []
        skip_incoming = False
        skip_current = False
        
        for line in content:
            if line.startswith(">>>>>>"):
                skip_incoming = True  # Start of incoming changes
                continue
            elif line.startswith("<<<<<<"):
                skip_incoming = False  # End of incoming changes
                continue
            if skip_incoming:
                incoming_changes.append(line)
            elif line.startswith("<<<<<<"):
                skip_current = True  # Start of current changes
                continue
            elif line.startswith(">>>>>>"):
                skip_current = False  # End of current changes
                continue
            if not skip_current:
                current_changes.append(line)

        # Create new content with both sections
        combined_content = current_changes + ["\n# Incoming Changes\n"] + incoming_changes

        # Write the combined content back to the file
        with open(file_path, 'w') as file:
            file.writelines(combined_content)

        self.stage_file(file_path)
        
    def continue_merge(self):
        """Finalize the merge process if all conflicts are resolved."""
        if not self.repo_manager.repo.index.diff("HEAD"):
            self.commit_resolution()
            print("Merge completed successfully.")
        else:
            print("Some conflicts are still unresolved.")
