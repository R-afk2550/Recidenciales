"""
URL configuration for Residents app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, UnitViewSet, ResidentViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'residents', ResidentViewSet, basename='resident')

app_name = 'residents'

urlpatterns = [
    path('', include(router.urls)),
]
