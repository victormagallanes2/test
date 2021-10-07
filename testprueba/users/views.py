from django.conf import settings
from django.contrib.auth.models import Group
from django.http import JsonResponse
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# from dreamaway.base.emails import send_mail

# from .models import User
# from .serializers import (
#     AuthenticatedUserSerializer,
#     ChangePasswordSerializer,
#     GroupListSerializer,
#     UserCreateAdminSerializer,
#     UserCreateSerializer,
#     UserDetailSerializer,
#     UserUpdateAdminSerializer,
#     UserUpdateSerializer,
#     ComunityUserSerializer,
# )
# from .services import UserService


# class AuthenticatedUserView(APIView):
#     permission_classes = (IsAuthenticated, )
#     https_methods = ['get', 'post']

#     def get(self, request):
#         serializer = AuthenticatedUserSerializer(request.user)
#         return JsonResponse(data=serializer.data, status=200)

#     def post(self, request):
#         serializer = AuthenticatedUserSerializer(request.user, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return JsonResponse(data=serializer.data, status=200)


# class UsersViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated, )
#     queryset = User.objects.all()
#     serializer_class = AuthenticatedUserSerializer
#     http_method_names = ['get', 'delete', 'post', 'put', 'patch']
#     filter_backends = [filters.SearchFilter, DjangoFilterBackend]
#     search_fields = ['username', 'email', 'first_name', 'last_name', 'first_name']
#     filterset_fields = {
#         'date_joined': ['gte', 'lte', 'date__gte', 'date__lte'],
#         'is_active': ['exact'],
#         'username': ['exact'],
#         'expert': ['exact'],
#         'roles': ['range']
#     }

#     def get_queryset(self):
#         queryset = self.queryset
#         roles = self.request.query_params.get('roles', None)
#         if roles is not None:
#             roles = roles.split(',')
#             elements = list(map(lambda x: int(x) if x.isdigit() else 0, roles))
#             queryset = queryset.filter(roles__in=elements)

#         return queryset

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return UserCreateAdminSerializer

#         return AuthenticatedUserSerializer


# class UserDetailAPI(RetrieveAPIView):
#     serializer_class = UserDetailSerializer
#     queryset = User.objects.all()


# class UserCreateAPI(CreateAPIView):
#     serializer_class = UserCreateSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user_service = UserService()
#         _ = user_service.register(email=request.data['email'], password=request.data['password'], request=request)
#         return JsonResponse(data={'users': ['confirmation email sended', ]}, status=200)


# class UserUpdateAPI(UpdateAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = UserUpdateSerializer
#     queryset = User.objects.filter()

#     def get_queryset(self):
#         return self.queryset.filter(email=self.request.user.email)


# class ChangePasswordView(UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         user = self.request.user
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             if not user.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

#             user.set_password(serializer.data.get("new_password"))
#             user.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#             }
#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserHelp(APIView):
#     permission_classes = (IsAuthenticated, )
#     https_methods = ['post']

#     def post(self, request):
#         message = request.data['message']
#         if not message:
#             return JsonResponse(data={'user': ['No send message'],}, status=401)

#         send_mail(
#             title='Ayuda',
#             template='users/help.html',
#             data={
#                 'content': message,
#                 'username': request.user.username,
#                 'email': request.user.email,
#                 'phone': request.user.phone
#             },
#             to_email=settings.SUPPORT_EMAIL
#         )
#         return JsonResponse(data={'user': ['Email send sussesfull'],}, status=200)


# class UserPostulation(APIView):
#     permission_classes = (IsAuthenticated, )
#     https_methods = ['post']

#     def post(self, request):
#         message = request.data['message']
#         if not message:
#             return JsonResponse(data={'user': ['No send message'],}, status=401)

#         username = request.user.username
#         email = request.user.email
#         phone = request.user.phone
#         send_mail(
#             title='Postulacion',
#             template='users/postulacion.html',
#             data={
#                 'content': message,
#                 'username': username,
#                 'email': email,
#                 'phone': phone
#             },
#             to_email=settings.DEFAULT_FROM_EMAIL
#         )
#         return JsonResponse(data={'user': ['Email send sussesfull'],}, status=200)


# class UserUpdateAdminAPI(UpdateAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = UserUpdateAdminSerializer
#     queryset = User.objects.all()

#     def partial_update(self, request, *args, **kwargs):
#         user = self.request.user
#         instance = self.queryset.get(pk=kwargs.get('pk'))
#         serializer = self.serializer_class(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         if request.data['old_password'] or request.data['new_password']:
#             if not user.check_password(request.data["old_password"]):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 user.set_password(request.data['new_password'])
#                 user.save()
#         return Response(serializer.data)


# class ComunityUserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = ComunityUserSerializer
#     http_method_names = ['get']