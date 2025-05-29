from accounts import serializers
from task_manager.models import Project


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name', 'description', 'owner')

        extra_kwargs = {
            "id": {"read_only": True},
        }


class ListProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'members')


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'members')