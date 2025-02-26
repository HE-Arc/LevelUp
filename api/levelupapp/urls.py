from django.urls import path
from levelupapp.views import Score

urlpatterns = [
    path("save-score/", Score.post, name="save-score"),
]
