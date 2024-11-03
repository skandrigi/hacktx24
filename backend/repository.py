from git import Repo

class RepositoryManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def is_git_repo(self):
        """Check if the given path is a Git repository."""
        return self.repo.git_dir is not None

    def get_files_status(self):
        """Get the status of each file in the repository."""
        status = {}
        for item in self.repo.index.diff(None):
            status[item.a_path] = item.change_type
        return status

    def get_branches(self):
        """Retrieve branch names in the repository."""
        return [branch.name for branch in self.repo.branches]

    def get_commit_history(self, branch):
        """Fetch commit history for a branch."""
        return list(self.repo.iter_commits(branch))

    def switch_branch(self, branch_name):
        """Switch to a specified branch."""
        self.repo.git.checkout(branch_name)
