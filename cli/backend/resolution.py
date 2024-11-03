class StagingManager:
    def __init__(self):
        self.resolved_content = []  # Store resolved lines for each file

    def resolve_conflict(self, conflict, choice):
        """Resolve a conflict based on user choice and append resolved lines."""
        if choice == "incoming":
            resolved = conflict["incoming"]
        elif choice == "current":
            resolved = conflict["current"]
        else:
            resolved = conflict["current"] + ["\n# Incoming Changes\n"] + conflict["incoming"]
        
        self.resolved_content.extend(resolved + ["\n"])  # Add newline after each resolved conflict

    def save_resolved_content(self, filename):
        """Save the resolved content back to the 'merge-conflicts' folder."""
        with open(f"merge-conflicts/resolved_{filename}", "w") as f:
            f.writelines(self.resolved_content)
        self.resolved_content = []  # Clear after saving to handle next file
