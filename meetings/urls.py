from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingViewSet

# Router automatically creates:
# GET    /api/meetings/       → list
# POST   /api/meetings/       → create
# GET    /api/meetings/:id/   → retrieve
# PUT    /api/meetings/:id/   → update
# DELETE /api/meetings/:id/   → destroy
router = DefaultRouter()
router.register(r'meetings', MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]