from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_manager.models import Project
from task_manager.permissions import IsOwner
from task_manager.serializers import ProjectCreateModelSerializer, ProjectUpdateModelSerializer, ProjectAddMembers, \
    ProjectListModelSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListModelSerializer
    permission_classes = (IsAuthenticated,)

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
        elif self.action == 'project_add_members':
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
            permission_classes=[IsAuthenticated, IsOwner])
    def project_add_members(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectAddMembers(data=request.data, instance=project, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
