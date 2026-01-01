from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class AnalyzePRRequest(BaseModel):
    repo_url : str
    pr_number : int
    github_token : Optional[str] = None


@app.post("/check_pr/")
async def start_task_request(task_request : AnalyzePRRequest):
    data = {
        "repo_url" : task_request.repo_url,
        "pr_number" : task_request.pr_number,
        "github_token" : task_request.github_token,

     }
    print(data)
    return {"task_id":"12", "status": "Task initiated!"}