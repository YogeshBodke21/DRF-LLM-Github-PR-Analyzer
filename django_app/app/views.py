from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.task import analyze_repo_task
from celery.result import AsyncResult
# Create your views here.

@api_view(["POST"])
def start_task(request):
    data = request.data
    repo_url = data.get("repo_url")
    pr_number = data.get("pr_number")
    github_token = data.get("github_token")
    task = analyze_repo_task.delay(repo_url, pr_number, github_token)
    return Response({
        "task_id": task.id,
        "status" :"Task Started"
    })


@api_view(["GET"])
def task_status_check(request, task_id):
    result = AsyncResult(task_id)
    response = {
        "task_id": str(task_id),
        "status": result.state,
    }

    if result.state == "SUCCESS":
        response["data"] = result.result   

    elif result.state == "FAILURE":
        response["error"] = str(result.result)

    return Response(response)

