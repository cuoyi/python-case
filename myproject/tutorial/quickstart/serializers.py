from django.contrib.auth.models import Group, User
from rest_framework import serializers

from quickstart.models import UserTest


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserTestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserTest
        fields = ['username', 'password']
