"""
URL configuration for Visitors app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitorViewSet, TemporaryCodeViewSet

router = DefaultRouter()
router.register(r'visitors', VisitorViewSet, basename='visitor')
router.register(r'codes', TemporaryCodeViewSet, basename='temporarycode')

app_name = 'visitors'

urlpatterns = [
    path('', include(router.urls)),
]
