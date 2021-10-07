import json
import pytest
import random
from django.urls import reverse
from dreamaway.api.tests.tests import BaseTestModelViewSet
from dreamaway.authentication.views import (AuthenticatedView,
                                            PasswordChangeAuthenticatedView,
                                            RecoveryPasswordView,
                                            RestorePasswordView,
                                            ConfirmationView)
from dreamaway.users.tests.factories import UserModelFactory
from dreamaway.users.models import User
from dreamaway.authentication.tools import (
    clear_pin,
    generate_pin,
    get_url_appkey,
    save_pin
)
import string


pytestmark = [pytest.mark.urls('dreamaway.authentication.urls'), pytest.mark.unit, pytest.mark.views, pytest.mark.django_db]


class TestAuthenticatedView(BaseTestModelViewSet):
    view = AuthenticatedView

    def test_get(self, rf, mocker):
        url = reverse('authentication_athenticated')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.get(
                url,
                content_type='application/json',
                HTTP_APP_KEY=app.app,
                HTTP_SECRET_KEY=app.secret,
                HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view()
        response = view(request).render()
        json_response = json.loads(response.content)
        print(json_response)
        assert response.status_code == 200


# class TestPasswordChangeAuthenticated(BaseTestModelViewSet):
#     view = PasswordChangeAuthenticatedView

#     def test_create(self, rf, mocker):
#         url = reverse('authentication_change_password')
#         app = self.create_or_get_app()
#         user = User.objects.create(username="Pepe", email="pepetruen@gmail.com", password="old_password123456")
#         tokens = self.get_user_token_pairs(user)
#         request_data = {
#                         "password": "newPassword12346",
#                         "old_password": "old_password123456",
                        
#                     }
#         request = rf.post(
#             url,
#             content_type='application/json',
#             data=request_data,
#             HTTP_APP_KEY=app.app,
#             HTTP_SECRET_KEY=app.secret,
#             HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
#         )
#         view = self.view.as_view()
#         response = view(request).render()
#         json_response = json.loads(response.content)
#         print(json_response)
#         assert response.status_code == 200


class TestRecoveryPassword(BaseTestModelViewSet):
    view = RecoveryPasswordView

    def test_create(self, rf, mocker):
        url = reverse('authentication_recovery_password')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request_data = {
                        "email": user.email,
                    }
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view()
        response = view(request).render()
        json_response = json.loads(response.content)
        print(json_response)
        assert response.status_code == 200


class TestRestorePasswordView(BaseTestModelViewSet):
    view = RestorePasswordView

    def test_create(self, rf, mocker):
        url = reverse('authentication_restore_password')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        pin = generate_pin(user=user, base=string.ascii_letters + string.digits, action='invitation')
        save_pin(user=user, code=pin, action='password')
        request_data = {
                        "token": pin,
                        "password": user.password,
                    }
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view()
        response = view(request).render()
        json_response = json.loads(response.content)
        print(json_response)
        assert response.status_code == 200


class TestConfirmationView(BaseTestModelViewSet):
    view = ConfirmationView

    def test_create(self, rf, mocker):
        url = reverse('authentication_confirmation')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        pin = generate_pin(user=user, base=string.ascii_letters + string.digits, action='invitation')
        request_data = {
                        "email": user.email,
                        "token": pin,
                    }
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view()
        response = view(request).render()
        json_response = json.loads(response.content)
        print(json_response)
        assert response.status_code == 200


