import conflict

with open("mock_conflict.txt", "r") as f:
    content = f.read()
    # print(content)
    c = conflict.ConflictDetector()
    a = c.parse_conflict_sections(content)
    print(a)
