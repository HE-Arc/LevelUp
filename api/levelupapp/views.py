from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ScoreSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


# Create your views here.

@csrf_exempt
@api_view(["POST"])
def save_score(request, format=None):
    serializer = ScoreSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
