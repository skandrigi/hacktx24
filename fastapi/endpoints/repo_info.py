from fastapi import FastAPI
import git

app = FastAPI()

class RepoInfo:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def get_last_commit_time(self):
        commit = self.repo.head.commit
        return commit.committed_datetime

    def get_last_commit_message(self):
        commit = self.repo.head.commit
        return commit.message

repo_info = RepoInfo(repo_path="path/to/your/repo")

@app.get("/repo_info")
async def read_last_commit():
    """Endpoint to get the last commit message and time."""
    last_commit_time = repo_info.get_last_commit_time()
    last_commit_message = repo_info.get_last_commit_message()
    return {
        "last_commit_time": last_commit_time,
        "last_commit_message": last_commit_message
    }
