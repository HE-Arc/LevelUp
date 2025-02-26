from django.urls import path
from levelupapp.views import save_score

urlpatterns = [
    path("save-score/", save_score, name="save-score"),
]
