from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from core.models import User
from core.permission import IsAuthorOrReadOnly
from core.serializer import UserCreateSerializer, UserRetrieveUpdateSerializer
from django.contrib.auth import authenticate, login


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        # Проверка старого пароля
        old_password = request.data.get('old_password')
        if not check_password(old_password, user.password):
            raise ValidationError({'old_password': 'Неверный старый пароль.'})

        # Проверка надежности нового пароля
        new_password = request.data.get('new_password')
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            raise ValidationError({'new_password': e.messages})

        # Изменение пароля
        user.set_password(new_password)
        user.save()

        return super().update(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             old_password = serializer.validated_data.get('old_password')
#             new_password = serializer.validated_data.get('new_password')
#             if self.object.check_password(old_password):
#                 self.object.set_password(new_password)
#                 self.object.save()
#                 # Вход пользователя после смены пароля
#                 user = authenticate(request, username=self.object.username, password=new_password)
#                 login(request, user)
#                 return Response({'message': 'Пароль успешно изменен'})
#             else:
#                 return Response({'error': 'Неверный старый пароль'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse(status=status.HTTP_200_OK)
