class ConflictDetector:
    def __init__(self):
        pass

    def get_conflict_line_ranges(self, file_lines):
        """Get line ranges for each conflict in a file.

        arguments:
            file_lines (list): List of lines in the file.

        returns:
            list: List of tuples, where each tuple is (start_line, end_line) for a conflict.
        """
        conflict_ranges = []
        start_line = None
        divider_line = None

        # Iterate over each line and keep track of line numbers
        for line_num, line in enumerate(file_lines):
            # Detect the start of a conflict
            if line.startswith("<<<<<<<"):
                start_line = line_num
            elif line.startswith("=======") and start_line is not None:
                divider_line = line_num
            elif line.startswith(">>>>>>>") and start_line is not None and divider_line is not None:
                # End of a conflict; store the range and reset
                end_line = line_num
                conflict_ranges.append((start_line, end_line))
                start_line = None
                divider_line = None

        return conflict_ranges

    def parse_conflict_sections(self, file_lines):
        """Extract conflicting sections as dictionaries of current and incoming changes.

        arguments:
            file_lines (list): List of lines in the file.

        will return:
            list: A list of dictionaries with "current" and "incoming" conflict sections.
        """
        conflict_sections = []
        current_section = []
        incoming_section = []
        in_conflict = False
        in_incoming = False

        for line in file_lines:
            if line.startswith("<<<<<<<"):
                in_conflict = True
                current_section = []
                incoming_section = []
            elif line.startswith("=======") and in_conflict:
                in_incoming = True
            elif line.startswith(">>>>>>>") and in_conflict:
                conflict_sections.append({
                    "current": current_section,
                    "incoming": incoming_section
                })
                in_conflict = False
                in_incoming = False
            elif in_conflict:
                if in_incoming:
                    incoming_section.append(line)
                else:
                    current_section.append(line)

        return conflict_sections
