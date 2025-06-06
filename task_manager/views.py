from celery.app import task

from config import celery_app
from celery.result import AsyncResult
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from task_manager.models import Project
from task_manager.permissions import IsOwner
from task_manager.serializers import ProjectCreateModelSerializer, ProjectUpdateModelSerializer, ProjectAddMembers, \
    ProjectListModelSerializer, TestCelerySerializer
from task_manager.tasks import add


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return self.queryset.filter(owner=self.request.user)
        elif self.action == 'my_project_members':
            return self.queryset.filter(members__exact=self.request.user)  # memberslarni ichida shu user bormi digani
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateModelSerializer
        if self.action in ['update', 'partial_update']:
            return ProjectUpdateModelSerializer
        if self.action == 'project_add_members':
            return ProjectAddMembers

        return self.serializer_class

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        if self.action == 'project_add_members':
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_project_add_members(self, serializer, project):
        return serializer.save(project=project)

    #  user azo bolgan projectlar va uzini projectlari
    @action(methods=['get'], detail=False, )
    def my_project_members(self, request, *args, **kwargs):
        project = self.get_queryset()
        serializer = ProjectListModelSerializer(project, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, serializer_class=ProjectAddMembers,
            permission_classes=[IsOwner, IsAuthenticated])
    def project_add_members(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectAddMembers(data=request.data, instance=project, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TestCeleryViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TestCelerySerializer

    @action(methods=['get'], detail=False, )
    def run_task(self, request):
        task = add.delay(12, 15)
        return Response({'task_id': task.id})

    @action(methods=['post'], detail=False, )
    def done_task(self, request):
        serializer = TestCelerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AsyncResult(serializer.validated_data['id'], app=celery_app)
        if result.ready():
            return Response({'result': result.result})
        return Response({'result': "processing"})
