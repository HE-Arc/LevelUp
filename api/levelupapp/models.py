from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max


class Game(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_leaderboard(self):
        best_scores = (
            self.score_set.values("user")
            .annotate(max_points=Max("points"))
            .order_by("-max_points")
        )

        top_scores = [
            self.score_set.filter(user=score["user"], points=score["max_points"]).first()
            for score in best_scores
        ]

        return top_scores

    def get_user_score(self, user) -> int | None:
        """Returns the position of the user in the leaderboard for this game, None if user not in leaderboard."""
        leaderboard = self.get_leaderboard()
        leaderboard_users = [score.user for score in leaderboard]
        if user in leaderboard_users:
            return [score.user for score in leaderboard].index(user) + 1
        return None



class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
