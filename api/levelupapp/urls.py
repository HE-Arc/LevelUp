from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from levelupapp import views

router = DefaultRouter()
router.register(r"games", views.GameViewSet, basename="game")

urlpatterns = [
    path("", include(router.urls)),
]