class StagingManager:
    def __init__(self):
        self.resolved_content = []  # Store resolved lines for each file

    def resolve_and_save(self, conflict, choice, filename):
        """Resolve a conflict based on user choice and save the resolved content to a file."""
        
        # Resolve conflict based on choice
        if choice == "incoming":
            resolved = conflict["incoming"]
        elif choice == "current":
            resolved = conflict["current"]
        else:
            resolved = conflict["current"] + ["\n# Incoming Changes\n"] + conflict["incoming"]
        
        # Store resolved lines
        self.resolved_content.extend(resolved + ["\n"])  # Add newline after each resolved conflict
        
        # Save the resolved content back to the original file
        with open(filename, "w") as f:
            f.writelines(self.resolved_content)
        
        # Clear resolved content for the next file
        self.resolved_content = []
