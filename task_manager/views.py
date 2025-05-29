from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from task_manager.models import Project
from task_manager.pagination import CustomPagination
from task_manager.serializers import CreateProjectSerializer, ListProjectSerializer, UpdateProjectSerializer

from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ListProjectSerializer
    model = Project
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['members']
    search_fields = ['name']
    ordering_fields = ['id']
    pagination_class = CustomPagination


    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateProjectSerializer
        return super().get_serializer_class()

    @action(methods=['get'], detail=False)
    def my_projects_members(self, request):
        projects = Project.objects.all()
        serializer = ListProjectSerializer(projects, many=True)
        return Response(serializer.data)
