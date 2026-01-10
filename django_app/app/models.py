from django.db import models

# Create your models here.
class PRAnalysisRequest(models.Model):
    status_choices = [
        ("PENDING", "PENDING"), 
        ("PROCESSING", "PROCESSING"), 
        ("SUCCESS", "SUCCESS"), 
        ("FAILED", "FAILED")
        ]    
    repo_url = models.URLField()
    pr_number = models.PositiveIntegerField()
    task_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=status_choices, default="PENDING")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ("repo_url", "pr_number")

    def __str__(self):
        return f"PR NUmber - {self.pr_number} | Link - {self.repo_url}"


class PRAnalysisResult(models.Model):
    request = models.OneToOneField(PRAnalysisRequest, on_delete=models.CASCADE, related_name="analysis")
    llm_result = models.JSONField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.request.repo_url} - PR Number - {self.request.pr_number}"

