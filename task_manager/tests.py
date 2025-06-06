from django.test import TestCase
from rest_framework.permissions import BasePermission


# Create your tests here.
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner