from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, ActivationSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('аккаунт успешно создан', status=201)


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('аккаунт успешно активирован', status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer