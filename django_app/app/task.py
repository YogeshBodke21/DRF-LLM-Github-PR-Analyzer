from celery import shared_task, Celery
from app.utils.github import analyze_llm_response


app = Celery("django_app")

app.config_from_object('django.conf:settings', namespace="CELERY")


@shared_task
def analyze_repo_task(repo_url, pr_number, github_token):
    result = analyze_llm_response(repo_url, pr_number, github_token)
    print("result--->", result)
    return result
