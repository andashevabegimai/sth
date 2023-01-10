from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from account.utils import send_activation_code

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'пользователь с таким имейлом уже существует'

            )
        return email

    def validate(self, attr):
        password = attr.get('password')
        password2 = attr.pop('password_confirm')
        if password != password2:
            raise serializers.ValidationError('пароли не совпадают')
        return attr

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.mail, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()
    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not User.objects.filter(email=email, send_activation_code=code).exists():
            raise serializers.ValidationError('пользователь не найден')
        return data
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('пользователь не найден')
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError('не верный имейл или пароль')
        else:
            raise serializers.ValidationError('имейл и пароль обязательны к заполнению')
        data['user'] = user
        return data
