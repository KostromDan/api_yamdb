from random import randint

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',
                  )

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    email = EmailField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  )

    def create(self, validated_data):
        confirmation_code = str(randint(100000000, 999999999))
        user = User.objects.create(**validated_data,
                                   role='user',
                                   confirmation_code=confirmation_code)
        send_mail('Conformation code.', confirmation_code, 'mail@test.ru',
                  [user.email])
        print(confirmation_code)
        return user

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                f'Нельзя создать пользователя с именем <{value}>!')
        if User.objects.filter(username=value).exists():
            raise ValidationError(
                'Пользователь с данным логином уже существует!')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(
                'Пользователь с данной почтой уже существует!')
        return value
