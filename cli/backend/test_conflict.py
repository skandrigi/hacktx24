from conflict import ConflictDetector  

class MockRepositoryManager:
    def get_files_status(self):
        return {'mock_conflict.txt': 'U'}

repo_manager = MockRepositoryManager()
conflict_detector = ConflictDetector(repo_manager)

file_path = 'mock_conflict.txt'
conflicts = conflict_detector.detect_conflicts()

if file_path in conflicts:
    conflict_lines = conflict_detector.get_conflict_lines(file_path)
    print(f"Conflict markers in '{file_path}':", conflict_lines)

    conflict_sections = conflict_detector.parse_conflict_sections(file_path)
    for section in conflict_sections:
        print("Current changes:\n", "".join(section["current"]))
        print("Incoming changes:\n", "".join(section["incoming"]))
else:
    print("No conflicts detected.")
