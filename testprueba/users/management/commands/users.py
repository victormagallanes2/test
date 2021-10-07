import csv

from django.core.management.base import BaseCommand

from dreamaway.authorization.models import Role
from dreamaway.users.models import User


class Command(BaseCommand):
    help = 'command for user configuration'

    def handle(self, *args, **options):
        print('Data for \'users\':')
        with open('dreamaway/users/data/users.csv', encoding='utf-8') as file:
            users = csv.DictReader(file)
            for user in users:
                _user = User.objects.create(
                    email=user['email'],
                    username=user['username'],
                    first_name=user['first_name'],
                    last_name=user['last_name']
                )
                _user.is_active = True if user['is_active'] == 'True' else False
                _user.is_staff = True if user['is_staff'] == 'True' else False
                _user.is_superuser = True if user['is_superuser'] == 'True' else False
                _user.set_password(user['password'])
                try:
                    role = Role.objects.get(nemonic=user['role'])
                    _user.roles.add(role)
                except Role.DoesNotExist:
                    pass

                _user.save()

        print('  Applying users.User... OK')
