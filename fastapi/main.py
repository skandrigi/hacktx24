from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()
    
class FileInfo(BaseModel):
    repoPath: str
    filePath: str

@app.post("/handle_file_info")
async def handle_file_info(file_info: FileInfo):
    repo_path = file_info.repoPath
    file_path = file_info.filePath

class Backend:
    def __init__(self, message, repo_path):
        self.message = message
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path) 

    def get_last_commit_time(self):
        """Fetches the timestamp of the last commit."""
        commit = self.repo.head.commit
        return commit.committed_datetime

    def get_last_commit_message(self):
        """Fetches the message of the last commit."""
        commit = self.repo.head.commit
        return commit.message

    def feed_to_model_post(self, last_commit_time, message):
        """Simulates feeding data to a model (placeholder)."""
        # Placeholder for model interaction - you might call an ML model here.
        return f"Data fed to model: Time - {last_commit_time}, Message - {message}"

    def get_model_response(self):
        """Simulates getting a response from a model."""
        # Placeholder for getting a response from the model
        return "Model response placeholder."

backend = Backend(message="", repo_path="path/to/your/repo")

@app.get("/")
async def read_last_commit():
    """Endpoint to get the last commit message and time."""
    last_commit_time = backend.get_last_commit_time()
    last_commit_message = backend.get_last_commit_message()
    return {
        "last_commit_time": last_commit_time,
        "last_commit_message": last_commit_message
    }

@app.post("/feed_to_model")
async def feed_to_model():
    """Endpoint to feed commit data to the model."""
    last_commit_time = backend.get_last_commit_time()
    last_commit_message = backend.get_last_commit_message()
    response = backend.feed_to_model_post(last_commit_time, last_commit_message)
    return {"model_feed_response": response}

@app.get("/model_response")
async def get_model_response():
    """Endpoint to get a response from the model."""
    response = backend.get_model_response()
    return {"model_response": response}
