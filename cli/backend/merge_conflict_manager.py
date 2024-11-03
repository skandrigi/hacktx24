import os

class MergeConflictManager:
    def __init__(self, conflicts_folder="merge-conflicts"):
        self.conflicts_folder = conflicts_folder

    def load_conflict_files(self):
        """Load and return the contents of each text file in the conflicts folder."""
        conflicts = {}
        for filename in os.listdir(self.conflicts_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.conflicts_folder, filename), "r") as f:
                    conflicts[filename] = f.readlines()  # Read file lines as text
        return conflicts
