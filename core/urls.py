from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "UP"})


def evaluation(request):
    return JsonResponse({
        "candidateName": "Ananth M",
        "email": "ananthmadhusoodanan1@gmail.com",
        "repositoryUrl": "https://github.com/ananthmadhusoodanan/hintro-meeting-intelligence",
        "deployedUrl": "https://hintro-meeting-intelligence-t38v.onrender.com",
        "externalIntegration": "Email via Resend",
        "features": [
            "JWT Authentication",
            "Meeting Management with Pagination",
            "AI Analysis with Citations (Groq/LLaMA)",
            "Action Item Management",
            "Overdue Detection",
            "Scheduled Email Reminders",
            "Unified API Response Format",
            "Request Trace ID",
            "Swagger Documentation"
        ]
    })


def setup_admin(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'ananthmadhusoodanan1@gmail.com', 'Admin@1234')
        return JsonResponse({"status": "created"})
    return JsonResponse({"status": "already exists"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('meetings.urls')),
    path('api/', include('action_items.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('health/', health_check, name='health'),
    path('api/evaluation/', evaluation, name='evaluation'),
    path('setup-admin/', setup_admin),
]
