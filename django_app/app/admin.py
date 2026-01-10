from django.contrib import admin
from .models import PRAnalysisRequest, PRAnalysisResult
# Register your models here.


admin.site.register(PRAnalysisRequest)
admin.site.register(PRAnalysisResult)
