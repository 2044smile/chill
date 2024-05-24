from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'hall', views.HallViewSet, basename='hall')
router.register(r'student', views.StudentViewSet, basename='student')


urlpatterns = [
    path('', include(router.urls))
]
