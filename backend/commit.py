class CommitComparer:
    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def compare_latest_commits(self, branch1, branch2):
        """Compare the latest commits of two branches to identify the more recent one."""
        commit1 = next(self.repo_manager.get_commit_history(branch1))
        commit2 = next(self.repo_manager.get_commit_history(branch2))
        if commit1.committed_date > commit2.committed_date:
            return branch1
        else:
            return branch2

    def get_commit_message(self, branch):
        """Retrieve the latest commit message from a branch."""
        commit = next(self.repo_manager.get_commit_history(branch))
        return commit.message

    def get_commit_time(self, branch):
        """Retrieve the timestamp of the latest commit from a branch."""
        commit = next(self.repo_manager.get_commit_history(branch))
        return commit.committed_date
