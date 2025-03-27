from rest_framework import serializers
from levelupapp.models import Game, Score


class ScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'game', 'user', 'username', 'points', 'date']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = [
            "url",
            "id",
            "name",
        ]
