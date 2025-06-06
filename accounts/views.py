from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import UserSerializer, ListUserSerializer


# Create your views here.

class RegisterApiview(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                'Success', UserSerializer
            )
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data)


class UpdateView(APIView):

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListUsersView(GenericViewSet, ListModelMixin):
    queryset = User.objects.all()
    model = User
    serializer_class = ListUserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
