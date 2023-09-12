from rest_framework import serializers
from rest_framework.serializers import *
from .models import *
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model
User = get_user_model()


class TimeLapseSerializer(ModelSerializer):
    class Meta:
        model = TimeLapse
        fields = '__all__'


#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ['url', 'username', 'email', 'password', 'id', 'first_name', 'last_name']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'id', 'first_name', 'last_name', 'phone', 'balance']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model()(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user
