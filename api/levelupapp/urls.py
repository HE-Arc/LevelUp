from django.urls import path
from levelupapp.views import ScoreView

urlpatterns = [
    path("save-score/", ScoreView.post, name="save-score"),
]
