from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.task import analyze_repo_task
from celery.result import AsyncResult
from django_redis import get_redis_connection
from .models import PRAnalysisRequest, PRAnalysisResult
from .serializers import PRAnalysisSerializer
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

@swagger_auto_schema(
        method = "post",
        request_body=PRAnalysisSerializer,
        response = {200 : "Task Started"}
)
@api_view(["POST"])
def start_task(request):
    data = request.data
    repo_url = data.get("repo_url")
    pr_number = data.get("pr_number")
    github_token = data.get("github_token")
    #database logic goes here..
    if not repo_url or not pr_number or not github_token:
        return Response({"error":"Repo_URL, PR_Number and Github_token are required"},
                        status= status.HTTP_400_BAD_REQUEST )

    pr_request, created = PRAnalysisRequest.objects.get_or_create(
        repo_url = repo_url,
        pr_number = pr_number,
        defaults={"status":"PENDING"}
    )
    print("Repo registered!!")
    #if it exist, it will save status as PENDING
    if not created:
        pr_request.status = "PENDING"
        pr_request.save()


    task = analyze_repo_task.delay(repo_url, pr_number, github_token)
    pr_request.task_id = task.id
    pr_request.status = "PROCESSING"
    pr_request.save()
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

#commands
#celery - celery -A django_app worker -l info