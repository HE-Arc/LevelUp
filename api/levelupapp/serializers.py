from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            "url",
            "user",
            "game",
            "points",
        ]
