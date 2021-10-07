from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    # AuthenticatedView,
    # ConfirmationView,
    MyTokenObtainPairView,
    # PasswordChangeAuthenticatedView,
    # RecoveryPasswordView,
    # RestorePasswordView
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='authentication_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='authentication_token_refresh'),
    # path('password/', PasswordChangeAuthenticatedView.as_view(), name='authentication_change_password'),
    # path('recovery/', RecoveryPasswordView.as_view(), name='authentication_recovery_password'),
    # path('restore/', RestorePasswordView.as_view(), name='authentication_restore_password'),
    # path('confirmation/', ConfirmationView.as_view(), name='authentication_confirmation'),
    # path('authenticated/', AuthenticatedView.as_view(), name='authentication_athenticated')
]
