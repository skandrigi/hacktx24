class ConflictDetector:
    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def detect_conflicts(self):
        """Detect files with conflict markers."""
        conflicts = []
        for file_path, status in self.repo_manager.get_files_status().items():
            if status == "U" or self.has_conflict_markers(file_path):  # Check Git status or markers
                conflicts.append(file_path)
        return conflicts

    def has_conflict_markers(self, file_path):
        """Check if a file contains conflict markers."""
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return all(marker in content for marker in ["<<<<<<<", "=======", ">>>>>>>"])
        except FileNotFoundError:
            return False

    def get_conflict_lines(self, file_path):
        """Identify lines with conflict markers in a specific file."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        conflict_markers = {"start": [], "divider": [], "end": []}
        for i, line in enumerate(lines):
            if line.startswith("<<<<<<<"):
                conflict_markers["start"].append(i)
            elif line.startswith("======="):
                conflict_markers["divider"].append(i)
            elif line.startswith(">>>>>>>"):
                conflict_markers["end"].append(i)
        return conflict_markers

    def parse_conflict_sections(self, file_path):
        """Extract conflicting sections in a file."""
        conflict_lines = self.get_conflict_lines(file_path)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        sections = []
        for start, divider, end in zip(conflict_lines["start"], conflict_lines["divider"], conflict_lines["end"]):
            sections.append({
                "current": lines[start+1:divider],
                "incoming": lines[divider+1:end]
            })
        return sections
