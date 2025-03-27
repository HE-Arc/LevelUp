import json

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CreateUserForm
from .models import Game, Score
from .score_utils import ScoreUtils
from .serializers import ScoreSerializer, GameSerializer


@ensure_csrf_cookie
@require_http_methods(["GET"])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE", "")})


@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        identifier = data.get("email")  # Peut être un email ou un username
        password = data["password"]
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

    user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier).first()

    if user and user.check_password(password):
        login(request, user)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)


def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@require_http_methods(["GET"])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse({"id": request.user.id, "username": request.user.username, "email": request.user.email})
    return JsonResponse({"message": "Not logged in"}, status=401)


@require_http_methods(["POST"])
def register(request):
    data = json.loads(request.body.decode("utf-8"))
    form = CreateUserForm(data)

    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"success": "User registered successfully"}, status=201)
        except IntegrityError:
            return JsonResponse({"error": "Cet email ou nom d'utilisateur est déjà utilisé."}, status=400)
    else:
        errors = form.errors.as_json()
        return JsonResponse({"error": errors}, status=400)


@api_view(["POST"])
def save_score(request):
    data = request.data
    data["game"] = Game.objects.get(name=request.data["game"]).id
    serializer = ScoreSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def leaderboard(request):
    game_name = request.GET.get("game_name")

    try:
        game = Game.objects.get(name=game_name)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    top_scores = game.get_leaderboard()
    serializer = ScoreSerializer(top_scores, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def rank_score_sum(request) -> Response(dict[str, int]):
    """
    Returns the total rank score for the user_id specified GET parameters.
    """

    user_id = request.GET.get("user_id")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    rank_score_sum = 0

    for game in Game.objects.all():
        rank = game.get_user_rank(user)
        if rank is None:
            continue

        rank_score_sum += ScoreUtils.rank_score(rank)

    return Response(
        {
            "rank_score_sum": rank_score_sum,
        }
        , status=status.HTTP_200_OK
    )


@api_view(["GET"])
def user_full_score(request) -> Response(dict[str, dict[str, int | float]]):
    """
    Returns everything related to the score of the user corresponding to this user_id passed in GET parameters
    - Score and rank and rank score for each game
    - Average rank on all played games
    - Sum of rank score
    - Rank of rank score
    """

    user_id = request.GET.get("user_id")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    scores = {}
    for score in Score.objects.filter(user_id=user_id):
        scores[score.game.name] = score.points

    ranks = {}
    rank_sum = 0
    rank_scores = {}
    rank_score_sum = 0
    nb_games = 0

    for game in Game.objects.all():
        rank = game.get_user_rank(user)
        if rank is None:
            continue

        score = ScoreUtils.rank_score(rank)

        ranks[game.name] = rank
        rank_scores[game.name] = score

        rank_sum += rank
        rank_score_sum += score

        nb_games += 1

    return Response(
        {
            "scores": scores,
            "ranks": ranks,
            "rank_avg": rank_sum / nb_games if nb_games > 0 else 0,
            "rank_scores": rank_scores,
            "rank_score_sum": rank_score_sum,
            "rank_score_rank": ScoreUtils.rank_score_rank(user)
        }
        , status=status.HTTP_200_OK
    )


@api_view(["GET"])
def rank_score_leaderboard(request):
    rsl = ScoreUtils.rank_score_leaderboard()

    rsl = [{"username": entry[0].username, "rank_score": entry[1]} for entry in rsl]

    return Response(
        rsl
        , status=status.HTTP_200_OK
    )


@api_view(["GET"])
def rank_score_rank(request):
    user_id = request.GET.get("user_id")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(
        {
            "rank_score_rank": ScoreUtils.rank_score_rank(user)
        }
        , status=status.HTTP_200_OK
    )


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
