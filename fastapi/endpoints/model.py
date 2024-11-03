from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

class ModelInterface:
    def send_to_model(self, last_commit_time: datetime, message: str):
        #
        return f"Data sent to model: Time - {last_commit_time}, Message - {message}"

    def get_response(self):
        #
        return "Model response placeholder."

model_interface = ModelInterface()

@app.post("/feed_to_model")
async def feed_to_model(last_commit_time: datetime, message: str):
    """Endpoint to feed commit data to the model."""
    response = model_interface.send_to_model(last_commit_time, message)
    return {"model_feed_response": response}

@app.get("/model_response")
async def get_model_response():
    """Endpoint to get a response from the model."""
    response = model_interface.get_response()
    return {"model_response": response}
