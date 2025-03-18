import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ScoreSerializer, GameSerializer
from .forms import CreateUserForm
from .models import Game, Score


@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE", "")})


@require_http_methods(['POST'])
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


@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse({"id": request.user.id, "username": request.user.username, "email": request.user.email})
    return JsonResponse({"message": "Not logged in"}, status=401)


@require_http_methods(['POST'])
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


@api_view(['POST'])
def save_score(request):
    serializer = ScoreSerializer(data=request.data, context={"request": request})
    print("test")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def leaderboard(request):
    game_id = request.GET.get("game_id")

    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    top_scores = game.get_leaderboard()
    serializer = ScoreSerializer(top_scores, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
