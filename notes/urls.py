from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet
from .auth_views import current_user

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/user/', current_user, name='current_user'),
]