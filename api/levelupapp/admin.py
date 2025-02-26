from django.contrib import admin

from levelupapp.models import Game, ScoreView


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(ScoreView)
class ScoreAdmin(admin.ModelAdmin):
    pass
