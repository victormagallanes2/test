import string

from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

#from dreamaway.base.emails import send_mail
#from dreamaway.users.models import User

#from .models import Pin
from .serializers import (
    #ConfirmationSerializer,
    MyTokenObtainPairSerializer,
    # PasswordChangeSerializer,
    # RecoveryPasswordSerializer,
    # RestorePasswordSerializer,
)
#from .tools import generate_pin, get_url_appkey


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AuthenticatedView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if self.request.user.picture:
            picture = self.request.user.picture.url
        else:
            picture = self.request.user.avatar
        data = {
            'id': self.request.user.id,
            'is_superuser': self.request.user.is_superuser,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'picture': picture,
            'email': self.request.user.email,
            'roles': []
        }
        return Response(data=data, status=HTTP_200_OK)


# class PasswordChangeAuthenticatedView(APIView):
#     permission_classes = (IsAuthenticated, )

#     def post(self, request):
#         serializer = PasswordChangeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if check_password(serializer.data['old_password'], self.request.user.password):
#             self.request.user.set_password(serializer.data['password'])
#             self.request.user.save()
#             return Response(data={'user': ['Contraseña guardada']})

#         return Response(
#             data={'user': ['Credenciales incorrectas']},
#             status=HTTP_400_BAD_REQUEST
#         )


# class RecoveryPasswordView(APIView):
#     permission_classes = (AllowAny, )

#     def post(self, request):
#         serializer = RecoveryPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = get_object_or_404(User, email=serializer.data['email'])
#         pin = generate_pin(user=user, base=string.ascii_letters + string.digits, action='password', digits=32)
#         send_mail(
#             title='Recuperar Contraseña | Dreamaway',
#             template='recovery_password.html',
#             data={
#                 'url_from': f'{get_url_appkey(request.headers)}/change/password/{pin}',
#                 'full_name': user.full_name
#             },
#             to_email=user.email
#         )
#         return Response(data={'user': ['mail has been sent']})


# class RestorePasswordView(APIView):
#     permission_classes = (AllowAny, )

#     def post(self, request):
#         serializer = RestorePasswordSerializer(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         pin = get_object_or_404(Pin, code=serializer.data['token'], action='password')
#         if pin.is_valid():
#             pin.user.set_password(serializer.data['password'])
#             pin.user.is_active = True
#             pin.user.save()
#             pin.delete()

#             return Response(data={'user': ['Contraseña actualizada correctamente']})

#         return Response(data={'user': ['Token no válido']}, status=HTTP_400_BAD_REQUEST)


# class ConfirmationView(APIView):
#     permission_classes = (AllowAny, )

#     def post(self, request):
#         serializer = ConfirmationSerializer(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         user = get_object_or_404(User, email=serializer.data['email'])
#         pin = get_object_or_404(Pin, user=user, code=request.data['token'])
#         if pin.is_valid():
#             user.is_active = True
#             user.save()
#             pin.delete()
#             return Response(data={'user': ['Email confirmado correctamente']})

#         return Response(data={'user': ['Token no válido']}, status=HTTP_400_BAD_REQUEST)
