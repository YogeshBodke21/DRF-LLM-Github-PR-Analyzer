from rest_framework import serializers
from .models import PRAnalysisRequest


class PRAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRAnalysisRequest
        fields = "__all__"