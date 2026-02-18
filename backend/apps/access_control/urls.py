"""
URL configuration for Access Control app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccessPointViewSet, AccessCodeViewSet

router = DefaultRouter()
router.register(r'points', AccessPointViewSet, basename='accesspoint')
router.register(r'codes', AccessCodeViewSet, basename='accesscode')

app_name = 'access_control'

urlpatterns = [
    path('', include(router.urls)),
]
