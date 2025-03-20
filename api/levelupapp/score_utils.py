from django.contrib.auth.models import User
from .models import Game

class ScoreUtils:
    @staticmethod
    def rank_score(rank):
        """
        Returns the rank score corresponding to the given rank.
        Rank score allows comparison of score across different games.
        """
        return 100 / (rank ** .5)

    @staticmethod
    def rank_score_leaderboard():
        """Returns an array of users and the corresponding rank score, sorted by rank score."""
        user_scores = {}
        for user in User.objects.all():
            user_total_score = 0
            for game in Game.objects.all():
                rank = game.get_user_rank(user)
                if rank is None:
                    continue
                user_total_score += ScoreUtils.rank_score(rank)
            user_scores[user] = user_total_score
        return sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    @staticmethod
    def rank_score_rank(user):
        """Returns the rank of the rank score corresponding to the given user in the rank score leaderboard."""
        rank_score_leaderboard = ScoreUtils.rank_score_leaderboard()
        users = [row[0] for row in rank_score_leaderboard]
        if user in users:
            return users.index(user) + 1
        return None