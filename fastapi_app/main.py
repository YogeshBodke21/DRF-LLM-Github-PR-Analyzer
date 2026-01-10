from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import httpx

app = FastAPI()

class AnalyzePRRequest(BaseModel):
    repo_url : str
    pr_number : int
    github_token : Optional[str] = None


DJANGO_API_URL = "http://127.0.0.1:8001"

# @app.post("/check_pr/")
# async def start_task_request(task_request : AnalyzePRRequest):
#     data = {
#         "repo_url" : task_request.repo_url,
#         "pr_number" : task_request.pr_number,
#         "github_token" : task_request.github_token,

#      }
#     print(data)
#     return {"task_id":"12", "status": "Task initiated!"}


@app.post("/start_task/")
async def start_task_request(task_request: AnalyzePRRequest):
    """
    Trigger the task in Django and return the task ID.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DJANGO_API_URL}/start_task/",
            data={
                "repo_url": task_request.repo_url,
                "pr_number": task_request.pr_number,
                "github_token": task_request.github_token,

            }
        )
        if response.status_code != 200:
            return {"error": "Failed to start task", "details": response.text}
        task_id = response.json().get("task_id")
        return {"task_id": task_id, "status": "Task started"}



@app.get("/status_check/{task_id}")
async def task_status_check(task_id : str):
    """
    Check the status of task by passing the task id.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DJANGO_API_URL}/status_check/{task_id}/",
        )
        if response.status_code != 200:
            return {"error": "Failed to start task", "details": response.text}
        response = response.json()
        return {"Response": response}
