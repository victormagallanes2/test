from django.contrib.auth.models import Permission
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from testprueba.users.models import User


class MyTokenObtainSerializerCustom(serializers.Serializer):
    username_field = User.EMAIL_FIELD
    user = None

    def __init__(self, *args, **kwargs):
        super(MyTokenObtainSerializerCustom, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        self.user = User.objects.filter(email=attrs[self.username_field]).first()

        if not self.user:
            raise exceptions.AuthenticationFailed('The user is not valid')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise exceptions.AuthenticationFailed('Incorrect credentials.')

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class MyTokenObtainPairSerializer(MyTokenObtainSerializerCustom):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['username'] = self.user.username
        # if self.user.picture:
        #     data['picture'] = self.user.picture.url
        # else:
        #     data['picture'] = ''

        # data['groups'] = self.user.groups.values_list('name', flat=True)
        # permissions_list = self.user.groups.values_list('permissions', flat=True)
        # dic = {}
        # option = []
        # for id_permissions in permissions_list:
        #     obj = Permission.objects.get(id=id_permissions)
        #     option.append(str(obj.name))
        #     option2 = set(option)
        #     dic[str(obj.content_type)] = option2
        #     data['permissions'] = dic

        return data


# class PasswordChangeSerializer(serializers.Serializer):
#     password = serializers.CharField(required=True)
#     old_password = serializers.CharField(required=True)


# class RecoveryPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)


# class RestorePasswordSerializer(serializers.Serializer):
#     token = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)


# class ConfirmationSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     token = serializers.CharField(required=True)
