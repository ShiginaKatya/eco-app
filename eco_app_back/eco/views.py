# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import UserSerializer
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
