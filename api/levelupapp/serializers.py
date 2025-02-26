from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Score


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "name",
            "created_at",
            "updated_at",
        ]


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            "user",
            "game",
            "points",
        ]
