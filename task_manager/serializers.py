from rest_framework import serializers

from accounts.models import User
from task_manager.models import Project, Task


class ProjectListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members']


class ProjectCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'members', 'description',  ]


class ProjectUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'members', 'description',  ]


class ProjectAddMembers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['members']



class TestCelerySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)



