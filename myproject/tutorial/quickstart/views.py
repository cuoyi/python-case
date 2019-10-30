# Create your views here.
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from rest_framework import viewsets

from quickstart.models import UserTest
from quickstart.serializers import GroupSerializer, UserSerializer, UserTestSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserTestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = UserTest.objects.all()
    serializer_class = UserTestSerializer
