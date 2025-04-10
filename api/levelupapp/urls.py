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
    path("rank_score_sum", views.rank_score_sum, name="rank_score_sum"),
    path("user_full_score", views.user_full_score, name="user_full_score"),
    path("rank_score_leaderboard", views.rank_score_leaderboard, name="rank_score_leaderboard"),
    path("rank_score_rank", views.rank_score_rank, name="rank_score_rank"),
    path("records", views.records, name="records")
]
