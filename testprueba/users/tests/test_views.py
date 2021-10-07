import json
import pytest
import random
from django.urls import reverse
from dreamaway.api.tests.tests import BaseTestModelViewSet
from dreamaway.users.models import User
from dreamaway.users.serializers import AuthenticatedUserSerializer, ComunityUserSerializer
from dreamaway.users.views import (UsersViewSet,
                                   ComunityUserViewSet,
                                   UserCreateAPI,
                                   UserDetailAPI,
                                   UserUpdateAPI,
                                   UserUpdateAdminAPI,
                                   UserPostulation,
                                   UserHelp)
from dreamaway.users.tests.factories import UserModelFactory
from dreamaway.authorization.models import Role
from dreamaway.tags.models import Tag


pytestmark = [pytest.mark.urls('dreamaway.users.urls'), pytest.mark.unit, pytest.mark.views, pytest.mark.django_db]


class TestUser(BaseTestModelViewSet):
    view = UsersViewSet
    model_factory = UserModelFactory

    def test_list(self, rf, mocker):
        url = reverse('user-list')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        for x in range(0, 4):
            user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.get(
                url,
                content_type='application/json',
                HTTP_APP_KEY=app.app,
                HTTP_SECRET_KEY=app.secret,
                HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view({'get': 'list'})
        response = view(request).render()
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 5
    
    def test_retrieve(self, rf, mocker):
        roles = Role.objects.create(name='team', nemonic='sdj4446jsd')
        roles.save()
        expert = Tag.objects.create(name='Tema', description='description', nemonic='topic', lvl=1)
        expert.save()
        user = User.objects.create(**self.model_factory().prepare_data())
        user.roles.add(roles)
        user.expert.add(expert)
        expected_json = AuthenticatedUserSerializer(user).data
        url = reverse('user-detail', kwargs={'pk': user.id})
        app = self.create_or_get_app()
        tokens = self.get_user_token_pairs(user)
        request = rf.get(
                url,
                content_type='application/json',
                HTTP_APP_KEY=app.app,
                HTTP_SECRET_KEY=app.secret,
                HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view({'get': 'retrieve'})
        response = view(request, pk=user.id).render()
        json_response = json.loads(response.content)
        assert response.status_code == 200
        for field in ['email',
                      'username',
                      'first_name',
                      'last_name',
                      'phone',
                      'about_me',
                      'web_site',
                      'facebook',
                      'twitter',
                      'instagram',
                      'continental_region',
                      'country',
                      'city',
                      'id',
                      'is_superuser',
                      'is_active',
                      'roles',
                      #'expert',
                      'invitation_to_expert'
                      ]:
            assert json_response[field] == expected_json[field]
        for field in ['picture']:
            assert json_response[field][17:] == expected_json[field]

    def test_create_no_auth(self, rf, mocker):
        request_data = UserModelFactory().save_instance()
        url = reverse('user-list')
        app = self.create_or_get_app()
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
        )
        response = self.view.as_view({'post': 'create'})(request).render()
        json_response = json.loads(response.content)
        assert response.status_code == 401

    def test_create(self, rf, mocker):
        roles = Role.objects.create(name='developer', nemonic='vvpeki33')
        roles.save()
        request_data = {
                        "email": "lore@gmail.com",
                        "username": "lore",
                        "first_name": "Lorena",
                        "last_name": "Castillo",
                        "password": "12345678",
                        "roles": [roles.id]
                    }
        url = reverse('user-list')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        print(request_data)
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view({'post': 'create'})(request).render()
        json_response = json.loads(response.content)
        print(json_response)
        assert response.status_code == 201

        for field in ['email', 'username', 'first_name', 'last_name', 'password', 'roles']:
            assert json_response[field] == request_data[field]

    def test_create_empty_data(self, rf, mocker):
        request_data = dict()
        url = reverse('user-list')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view({'post': 'create'})(request).render()
        json_response = json.loads(response.content)

        assert response.status_code == 400 

        for field in ['email', 'username', 'password', 'roles']:
            assert field in json_response


    def test_partial_update(self, rf, mocker):
        new_user = User.objects.create(**self.model_factory().prepare_data())
        request_data = {
                        "email": "ruby@gmail.com",
                        "username": "ruby",
                        "first_name": "ruby",
                        "last_name": "ambar",
                    }
        url = reverse('user-detail', kwargs={'pk': new_user.id})
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.patch(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view({'patch': 'partial_update'})(request, pk=new_user.id).render()
        json_response = json.loads(response.content)
        assert response.status_code == 200

        assert json_response.get('id', False)
        for field in ['email', 'username', 'first_name', 'last_name']:
            assert json_response[field] == request_data[field]

    def test_update(self, rf, mocker):
        roles = Role.objects.create(name='team2', nemonic='sdj4446jsr')
        roles.save()
        new_user = User.objects.create(**self.model_factory().prepare_data())
        new_user.roles.add(roles)
        request_data = {
                        "email": "ruby2@gmail.com",
                        "username": "ruby2",
                        "first_name": "ruby2",
                        "last_name": "ambar2",
                        "roles": [roles.id],
                    }
        url = reverse('user-detail', kwargs={'pk': new_user.id})
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.put(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view({'put': 'update'})(request, pk=new_user.id).render()
        json_response = json.loads(response.content)
        print(json_response)
        assert response.status_code == 200

    def test_destroy_no_auth(self, rf, mocker):
        new_user = User.objects.create(**self.model_factory().prepare_data())
        url = reverse('user-detail', kwargs={'pk': new_user.id})
        app = self.create_or_get_app()
        request = rf.delete(
            url,
            content_type='application/json',
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
        )
        response = self.view.as_view({'delete': 'destroy'})(request, pk=new_user.id).render()

        assert response.status_code == 401


    def test_destroy(self, rf, mocker):
        new_user = User.objects.create(**self.model_factory().prepare_data())
        url = reverse('user-detail', kwargs={'pk': new_user.id})
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.delete(
            url,
            content_type='application/json',
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view({'delete': 'destroy'})(request, pk=new_user.id).render()

        assert response.status_code == 204
        assert not User.objects.filter(id=new_user.id).exists()


class TestComunity(BaseTestModelViewSet):
    view = ComunityUserViewSet
    model_factory = UserModelFactory

    def test_list(self, rf, mocker):
        url = reverse('user-list')
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        for x in range(0, 4):
            user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        request = rf.get(
                url,
                content_type='application/json',
                HTTP_APP_KEY=app.app,
                HTTP_SECRET_KEY=app.secret,
                HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view({'get': 'list'})
        response = view(request).render()
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 5
    
    def test_retrieve(self, rf, mocker):
        roles = Role.objects.create(name='team', nemonic='sdj4446jsd')
        roles.save()
        expert = Tag.objects.create(name='Tema', description='description', nemonic='topic', lvl=1)
        expert.save()
        user = User.objects.create(**self.model_factory().prepare_data())
        user.roles.add(roles)
        user.expert.add(expert)
        expected_json = ComunityUserSerializer(user).data
        url = reverse('user-detail', kwargs={'pk': user.id})
        app = self.create_or_get_app()
        tokens = self.get_user_token_pairs(user)
        request = rf.get(
                url,
                content_type='application/json',
                HTTP_APP_KEY=app.app,
                HTTP_SECRET_KEY=app.secret,
                HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view({'get': 'retrieve'})
        response = view(request, pk=user.id).render()
        json_response = json.loads(response.content)
        assert response.status_code == 200
        for field in [
                      'first_name',
                      'last_name',
                      'about_me',
                      'web_site',
                      'facebook',
                      'twitter',
                      'instagram',
                      'continental_region',
                      'country',
                      'city',
                      'id',
                      'invitation_to_expert'
                      ]:
            assert json_response[field] == expected_json[field]
        for field in ['picture']:
            assert json_response[field][17:] == expected_json[field]


class TestUserCreateAPI(BaseTestModelViewSet):
    view = UserCreateAPI
    model_factory = UserModelFactory

    def test_create(self, rf, mocker):
        roles = Role.objects.create(name='developer', nemonic='default')
        roles.save()
        request_data = {
                        "email": "lore@gmail.com",
                        "username": "lore",
                        "first_name": "Lorena",
                        "last_name": "Castillo",
                        "password": "12345678",
                        "roles": [roles.id]
                    }
        url = '/register/'
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(user)
        print(request_data)
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view()(request)

        assert response.status_code == 200


class TestUserDetailAPI(BaseTestModelViewSet):
    view = UserDetailAPI
    model_factory = UserModelFactory

    def test_retrieve(self, rf, mocker):
        roles = Role.objects.create(name='team', nemonic='sdj4446jsd')
        roles.save()
        expert = Tag.objects.create(name='Tema', description='description', nemonic='topic', lvl=1)
        expert.save()
        user = User.objects.create(**self.model_factory().prepare_data())
        user.roles.add(roles)
        user.expert.add(expert)
        expected_json = AuthenticatedUserSerializer(user).data
        url = str(user.id) + '/information/'
        app = self.create_or_get_app()
        tokens = self.get_user_token_pairs(user)
        request = rf.get(
                url,
                content_type='application/json',
                HTTP_APP_KEY=app.app,
                HTTP_SECRET_KEY=app.secret,
                HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        view = self.view.as_view()
        response = view(request, pk=user.id).render()
        json_response = json.loads(response.content)
        assert response.status_code == 200


class TestUserUpdateAPI(BaseTestModelViewSet):
    view = UserUpdateAPI
    model_factory = UserModelFactory

    def test_partial_update(self, rf, mocker):
        new_user = User.objects.create(**self.model_factory().prepare_data())
        request_data = {
                        "first_name": "ruby"
                    }
        url = str(new_user.id) + '/information/update/'
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(new_user)
        request = rf.patch(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view()(request, pk=new_user.id).render()
        json_response = json.loads(response.content)
        assert response.status_code == 200

    def test_update(self, rf, mocker):
        new_user = User.objects.create(**self.model_factory().prepare_data())
        roles = Role.objects.create(name='team', nemonic='sdj4446jsd')
        roles.save()        
        request_data = {
                        "email": "ruby2@gmail.com",
                        "username": "ruby2",
                        "first_name": "ruby2",
                        "last_name": "ambar2",
                        "roles": [roles.id],
                    }
        url = str(new_user.id) + '/information/update/'
        app = self.create_or_get_app()
        user = UserModelFactory().save_instance()
        tokens = self.get_user_token_pairs(new_user)
        request = rf.put(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view()(request, pk=new_user.id).render()
        json_response = json.loads(response.content)
        assert response.status_code == 200


class TestUserPostulation(BaseTestModelViewSet):
    view = UserPostulation
    model_factory = UserModelFactory

    def test_create(self, rf, mocker):
        user = UserModelFactory().save_instance()
        url = '/help/' + str(user.id)
        app = self.create_or_get_app()
        tokens = self.get_user_token_pairs(user)
        request_data = {
                        "message": "my message"

                    }
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view()(request)
        assert response.status_code == 200



class TestUserPostulation(BaseTestModelViewSet):
    view = UserPostulation
    model_factory = UserModelFactory

    def test_create(self, rf, mocker):
        user = UserModelFactory().save_instance()
        url = 'postulation/' + str(user.id)
        app = self.create_or_get_app()
        tokens = self.get_user_token_pairs(user)
        request_data = {
                        "message": "my message"

                    }
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view()(request)
        assert response.status_code == 200


class TestUserHelp(BaseTestModelViewSet):
    view = UserHelp
    model_factory = UserModelFactory

    def test_create(self, rf, mocker):
        user = UserModelFactory().save_instance()
        url = 'help/' + str(user.id)
        app = self.create_or_get_app()
        tokens = self.get_user_token_pairs(user)
        request_data = {
                        "message": "my message"

                    }
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data,
            HTTP_APP_KEY=app.app,
            HTTP_SECRET_KEY=app.secret,
            HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
        )
        response = self.view.as_view()(request)
        assert response.status_code == 200


# class TestUserUpdateAdminAPI(BaseTestModelViewSet):
#     view = UserUpdateAdminAPI
#     model_factory = UserModelFactory

#     def test_partial_update(self, rf, mocker):
#         new_user = User.objects.create(email="ruby2@gmail.com",
#                                        username="ruby2",
#                                        first_name="ruby2",
#                                        last_name="ambar2",
#                                        password="aSS844738384$$%")
#         request_data = {
#                         "old_password": new_user.password,
#                         "new_password": "Oommddd8384$dwww$%"
#                     }
#         url = '/configuration/' + str(new_user.id)
#         app = self.create_or_get_app()
#         user = UserModelFactory().save_instance()
#         tokens = self.get_user_token_pairs(new_user)
#         request = rf.patch(
#             url,
#             content_type='application/json',
#             data=request_data,
#             HTTP_APP_KEY=app.app,
#             HTTP_SECRET_KEY=app.secret,
#             HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access'])
#         )
#         response = self.view.as_view()(request, pk=new_user.id).render()
#         json_response = json.loads(response.content)
#         assert response.status_code == 200