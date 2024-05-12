from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (UserRegistrationSerializer, UserLoginSerializer,
                          UserProfileSerializer, UserChangePasswordSerializer,
                          SendPasswordResetEmailSerializer, UserPasswordResetSerializer)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, formate=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg': 'User registration successful', 'token': token}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, formate=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': 'User login successful', 'token': token}, status=status.HTTP_200_OK)
        else:
             return Response({'error': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, formate=None):
        serializer = UserProfileSerializer(request.user)
        # if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({'error':{'non_field_errors':['User not found']}}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, formate=None):
        serializers = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializers.is_valid(raise_exception=True)
        return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):

    def post(self, request, formate=None):
        serializers = SendPasswordResetEmailSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):

    def post(self, request, uid, token, formate=None):
        serailizer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serailizer.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset successful'}, status=status.HTTP_200_OK)
