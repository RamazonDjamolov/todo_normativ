from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


class TestAPIView(APIView):
    def get(self, request):
        username = [user.username for user in User.objects.all()]
        return Response( {"username": "salom"} )
