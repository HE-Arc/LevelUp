from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from levelupapp import views

router = DefaultRouter()
router.register(r"games", views.GameViewSet, basename="game")

urlpatterns = [
    path("", include(router.urls)),
    path('set-csrf-token', views.set_csrf_token, name=''),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('user', views.user, name='user'),
    path('register', views.register, name='register'),
]