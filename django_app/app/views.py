from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.task import analyze_repo_task
from celery.result import AsyncResult
from django_redis import get_redis_connection
# Create your views here.

@api_view(["POST"])
def start_task(request):
    data = request.data
    repo_url = data.get("repo_url")
    pr_number = data.get("pr_number")
    github_token = data.get("github_token")
    task = analyze_repo_task.delay(repo_url, pr_number, github_token)
    redis = get_redis_connection("default")
    # Store task_id with TTL(time to live) (e.g., 1 hour)
    redis.setex(
        f"task:{task.id}",
        3600,
        "created"
    )
    return Response({
        "task_id": task.id,
        "status" :"Task Started"
    })


@api_view(["GET"])
def task_status_check(request, task_id):
    redis = get_redis_connection("default")
    if not redis.exists(f"task:{task_id}"):
        return Response(
            {"error": "Invalid or expired task_id"},
            status=status.HTTP_404_NOT_FOUND
        )
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

