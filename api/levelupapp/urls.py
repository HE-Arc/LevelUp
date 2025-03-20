from django.urls import path, include
from levelupapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"games", views.GameViewSet, basename="game")
router.register(r"scores", views.ScoreViewSet, basename="score")

urlpatterns = [
    path("", include(router.urls)),
    path("set-csrf-token", views.set_csrf_token, name="set-csrf-token"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("user", views.user, name="user"),
    path("register", views.register, name="register"),
    path("save_score", views.save_score, name="save_score"),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path("user_overall_score", views.user_overall_score, name="user_overall_score"),
    path("user_full_score", views.user_full_score, name="user_full_score"),
]
