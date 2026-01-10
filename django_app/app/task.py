from celery import shared_task, Celery
from app.utils.github import analyze_llm_response
from .models import PRAnalysisResult, PRAnalysisRequest


app = Celery("django_app")

app.config_from_object('django.conf:settings', namespace="CELERY")

@shared_task()
def analyze_repo_task(repo_url, pr_number, github_token):
    pr_request = None

    try:
        result = analyze_llm_response(repo_url, pr_number, github_token)

        # Clean raw_output
        if isinstance(result, list):
            for file_result in result:
                file_result.get("Results", {}).pop("raw_output", None)

        print("Cleaned result --->", result)

        pr_request = PRAnalysisRequest.objects.get(
            repo_url=repo_url,
            pr_number=pr_number
        )

        PRAnalysisResult.objects.update_or_create(
            request=pr_request,
            defaults={"llm_result": result}
        )

        pr_request.status = "SUCCESS"
        pr_request.save(update_fields=["status"])

        return result

    except Exception as e:
        print("Celery task failed:", str(e))

        if pr_request:
            pr_request.status = "FAILED"
            pr_request.save(update_fields=["status"])

        raise e  # Important: lets Celery mark task as FAILED













































'''from celery import shared_task, Celery
from app.utils.github import analyze_llm_response
from .models import PRAnalysisResult, PRAnalysisRequest

app = Celery("django_app")

app.config_from_object('django.conf:settings', namespace="CELERY")


@shared_task
def analyze_repo_task(repo_url, pr_number, github_token):
    result = analyze_llm_response(repo_url, pr_number, github_token)
    if result:
        for file_result in result:
            if "Results" in file_result:
                file_result["Results"].pop("raw_output", None)
    print("result--->", result)
    try:
        print("----inside try of db")
        pr_request = PRAnalysisRequest.objects.get(repo_url=repo_url, pr_number=pr_number)
        PRAnalysisResult.objects.update_or_create(
            request = pr_request,
            defaults = { "llm_result" : result["Results"]}
        )
        pr_request.status = "SUCCESS"
        pr_request.save()
        print("----Status has been set to success!!")
        return result
    
    except Exception as e:
        pr_request.status = "FAILED"
        pr_request.save()
'''