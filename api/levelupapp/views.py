from rest_framework import viewsets

from levelupapp.models import Game
from levelupapp.serializers import GameSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer