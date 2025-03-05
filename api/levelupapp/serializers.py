from rest_framework import serializers
from levelupapp.models import Game, Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = [
            "url",
            "id",
            "name",
        ]
