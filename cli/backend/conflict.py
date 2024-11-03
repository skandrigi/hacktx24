class ConflictDetector:
    def detect_conflicts(self, file_lines):
        """Detect lines with conflict markers in the given lines."""
        conflicts = []
        in_conflict = False
        current = []
        incoming = []
        
        for line in file_lines:
            if line.startswith("<<<<<<<"):
                in_conflict = True
                current = []
            elif line.startswith("======="):
                incoming = []
            elif line.startswith(">>>>>>>"):
                conflicts.append({"current": current, "incoming": incoming})
                in_conflict = False
            elif in_conflict:
                if incoming:
                    incoming.append(line)
                else:
                    current.append(line)
        
        return conflicts

    def parse_conflict_sections(self, file_lines):
        """Extract conflict sections from lines for easier processing."""
        conflict_lines = self.detect_conflicts(file_lines)
        return [{"current": c["current"], "incoming": c["incoming"]} for c in conflict_lines]
