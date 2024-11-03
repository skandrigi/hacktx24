class StagingManager:
    def __init__(self):
        self.content = []
        self.first_conflict = {'current': [], 'incoming': []}
        self.found_first = False
        
    def parse_first_conflict(self, filename):
        """Parse only the first conflict from a file."""
        with open(filename, 'r') as f:
            self.content = f.readlines()
            
        in_conflict = False
        current_section = None
        
        for i, line in enumerate(self.content):
            if not self.found_first and line.startswith('<<<<<<< '):
                self.found_first = True
                in_conflict = True
                current_section = 'current'
                self.first_conflict['start_index'] = i
                continue
            elif self.found_first and line.startswith('======='):
                current_section = 'incoming'
                continue
            elif self.found_first and line.startswith('>>>>>>> '):
                self.first_conflict['end_index'] = i
                break
                
            if self.found_first and in_conflict and current_section:
                self.first_conflict[current_section].append(line)
    
    def resolve_and_save(self, choice, filename):
        """
        Resolve only the first conflict based on user choice and save the file.
        
        Args:
            choice (str): The resolution choice ('incoming', 'current', or 'both')
            filename (str): Path to the file being resolved
        """
        if not self.found_first:
            self.parse_first_conflict(filename)
            
        if not self.found_first:
            raise ValueError("No conflicts found in the file")
        
        # Resolve conflict based on choice
        if choice == "incoming":
            resolved = self.first_conflict["incoming"]
        elif choice == "current":
            resolved = self.first_conflict["current"]
        elif choice == "both":
            resolved = self.first_conflict["current"] + ["# Incoming Changes\n"] + self.first_conflict["incoming"]
        else:
            raise ValueError("Invalid choice. Must be 'incoming', 'current', or 'both'")

        # Replace the conflict with resolved content
        self.content[self.first_conflict['start_index']:self.first_conflict['end_index'] + 1] = resolved
        
        try:
            # Save the entire file with the resolved first conflict
            with open(filename, "w") as f:
                f.writelines(self.content)
        except IOError as e:
            raise IOError(f"Error writing to file {filename}: {str(e)}")