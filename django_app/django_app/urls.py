
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from app.views import task_status_check, start_task
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Github PR Analysis API",
        default_version="v1",
        description="API documentation for Github PR Analysis service",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Or IsAdminUser for admin-only
)

urlpatterns = [
    #Swagger UI
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),


    path("start_task/", start_task),
    path("status_check/<task_id>/", task_status_check),
    path('admin/', admin.site.urls),
]
