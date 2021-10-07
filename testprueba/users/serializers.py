from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import User


# class AuthenticatedUserSerializer(serializers.ModelSerializer):

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if instance.continental_region:
#             continental_region = {'id':'', 'name':''}
#             continental_region['id'] = instance.continental_region.id
#             continental_region['name'] = instance.continental_region.name
#             data['continental_region'] = continental_region

#         if instance.country:
#             country = {'id':'', 'name':''}
#             country['id'] = instance.country.id
#             country['name'] = instance.country.name
#             data['country'] = country

#         if instance.city:
#             city = {'id':'', 'name':''}
#             city['id'] = instance.city.id
#             city['name'] = instance.city.name
#             data['city'] = city

#         if data['picture'] is None:
#             data['picture'] = instance.avatar

#         user = User.objects.get(id=instance.id)
#         permissions_list = user.groups.values_list('permissions', flat=True)
#         dic = {}
#         option = []
#         for id_permissions in permissions_list:
#             obj = Permission.objects.get(id=id_permissions)
#             option.append(str(obj.name))
#             option2 = set(option)
#             dic[str(obj.content_type)] = option2
#             data['permissions'] = dic
#         data['expert'] = instance.expert.all().values()

#         return data

#     class Meta:
#         fields = (
#             'email', 'username', 'first_name', 'last_name', 'picture', 'phone', 'about_me', 'web_site', 'facebook',
#             'twitter', 'instagram', 'continental_region', 'country', 'city', 'id', 'is_superuser', 'is_active',
#             'last_login', 'date_joined', 'roles', 'expert','invitation_to_expert'
#         )
#         read_only_fields = ('is_superuser', 'is_active')
#         model = User


# class UserDetailSerializer(serializers.ModelSerializer):

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['roles'] = []
#         if instance.continental_region:
#             continental_region = {'id':'', 'name':''}
#             continental_region['id'] = instance.continental_region.id
#             continental_region['name'] = instance.continental_region.name
#             data['continental_region'] = continental_region

#         if instance.country:
#             country = {'id':'', 'name':''}
#             country['id'] = instance.country.id
#             country['name'] = instance.country.name
#             data['country'] = country

#         if instance.city:
#             city = {'id':'', 'name':''}
#             city['id'] = instance.city.id
#             city['name'] = instance.city.name
#             data['city'] = city

#         data['avatar'] = instance.avatar
#         if data['picture'] is None:
#             data['picture'] = instance.avatar
#         data['expert'] = instance.expert.all().values()
#         return data

#     class Meta:
#         model = User
#         fields = (
#             'id', 'username', 'first_name', 'last_name', 'email', 'phone', 'about_me', 'about_me', 'web_site',
#             'twitter', 'facebook', 'instagram', 'expert', 'interests', 'picture', 'invitation_to_expert'
#         )


# class UserUpdateSerializer(serializers.ModelSerializer):

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['roles'] = []
#         if instance.continental_region:
#             continental_region = {'id':'', 'name':''}
#             continental_region['id'] = instance.continental_region.id
#             continental_region['name'] = instance.continental_region.name
#             data['continental_region'] = continental_region

#         if instance.country:
#             country = {'id':'', 'name':''}
#             country['id'] = instance.country.id
#             country['name'] = instance.country.name
#             data['country'] = country

#         if instance.city:
#             city = {'id':'', 'name':''}
#             city['id'] = instance.city.id
#             city['name'] = instance.city.name
#             data['city'] = city

#         data['avatar'] = instance.avatar
#         if data['picture'] is None:
#             data['picture'] = instance.avatar
#         data['expert'] = instance.expert.all().values()
#         return data

#     class Meta:
#         model = User
#         fields = (
#             'username', 'first_name', 'last_name', 'email', 'picture', 'phone', 'about_me', 'continental_region',
#             'country', 'city', 'about_me', 'web_site', 'twitter', 'facebook', 'instagram', 'expert', 'interests', 'invitation_to_expert'
#         )


# class UserCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#         extra_kwargs = {
#             'username': {'required': False}
#         }


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


# class UserCreateAdminSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password', 'roles', 'picture', 'expert')


# class GroupListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Group
#         fields = ('__all__')


# class UserUpdateAdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         old_password = serializers.CharField(required=False)
#         new_password = serializers.CharField(required=False)
#         fields = ('first_name', 'last_name', 'email', 'is_superuser')

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['id'] = instance.id
#         data['roles'] = []
#         if instance.picture:
#             data['picture'] = instance.picture.url
#         else:
#             data['picture'] = 'https://dreamaway-01.s3.amazonaws.com/media/avatars/photo_2020-05-22_02-14-54.jpg'
#         return data


# class ComunityUserSerializer(serializers.ModelSerializer):

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if instance.continental_region:
#             continental_region = {'id':'', 'name':''}
#             continental_region['id'] = instance.continental_region.id
#             continental_region['name'] = instance.continental_region.name
#             data['continental_region'] = continental_region
#         if instance.country:
#             country = {'id':'', 'name':''}
#             country['id'] = instance.country.id
#             country['name'] = instance.country.name
#             data['country'] = country
#         if instance.city:
#             city = {'id':'', 'name':''}
#             city['id'] = instance.city.id
#             city['name'] = instance.city.name
#             data['city'] = city
#         if data['picture'] is None:
#             data['picture'] = instance.avatar
#         data['expert'] = instance.expert.all().values()
#         return data

#     class Meta:
#         fields = (
#             'first_name', 'last_name', 'picture', 'about_me', 'web_site', 'facebook',
#             'twitter', 'instagram', 'continental_region', 'country', 'city', 'id', 'expert','invitation_to_expert'
#         )
#         model = User