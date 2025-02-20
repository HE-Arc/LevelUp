from django.contrib import admin

from levelupapp.models import Game, Score

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass