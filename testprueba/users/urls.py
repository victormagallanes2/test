# from django.urls import path
# from rest_framework import routers

# from .views import (
#     UserCreateAPI,
#     UserDetailAPI,
#     UserHelp,
#     UserPostulation,
#     UsersViewSet,
#     UserUpdateAdminAPI,
#     UserUpdateAPI,
#     ComunityUserViewSet,
# )

# ROUTER = routers.SimpleRouter()
# ROUTER.register('users', UsersViewSet)
# ROUTER.register('comunity', ComunityUserViewSet)

# urlpatterns = [
#     path('register/', UserCreateAPI.as_view()),
#     path('<str:pk>/information/', UserDetailAPI.as_view()),
#     path('<str:pk>/information/update/', UserUpdateAPI.as_view()),
#     path('help/', UserHelp.as_view()),
#     path('postulation/', UserPostulation.as_view()),
#     path('configuration/<str:pk>/', UserUpdateAdminAPI.as_view())
# ]

# urlpatterns += ROUTER.urls
