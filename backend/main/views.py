import datetime

import django_filters
from rest_framework.viewsets import ModelViewSet
import rest_framework
from .models import TimeLapse
from rest_framework import generics

from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers

from django.contrib.auth import get_user_model
User = get_user_model()


class TimeLapseFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='date')
    id = filters.CharFilter(field_name='id')

    class Meta:
        model = TimeLapse
        fields = ['date', 'id']


#class UserFilter(filters.FilterSet):
#    username = filters.CharFilter(field_name='username')
#
#    class Meta:
#        model = User
#        fields = ['username']


class PlayerFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username')

    class Meta:
        model = User
        fields = ['username']


class TimeLapseViewSet(ModelViewSet):
    queryset = TimeLapse.objects.all()
    serializer_class = TimeLapseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimeLapseFilter

    def get_object(self):
        if 'pk' in self.kwargs:
            self.lookup_field = 'pk'
        elif 'id' in self.kwargs:
            self.lookup_field = 'id'

        return super(TimeLapseViewSet, self).get_object()


#class UserViewSet(ModelViewSet):
#    queryset = User.objects.all().order_by('-date_joined')
#    serializer_class = UserSerializer
#    filter_backends = [DjangoFilterBackend]
#    filterset_class = UserFilter

class PlayerViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlayerFilter


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = serializers.SignupSerializer
