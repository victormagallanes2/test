from django.db import models
from django.utils import timezone

# from dreamaway.users.models import User


# class Pin(models.Model):
#     ACTIONS = (
#         ('password', 'password'),
#         ('activate', 'activate'),
#         ('invitation', 'invitation')
#     )
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     date_created = models.DateTimeField(auto_now_add=True)
#     action = models.CharField(choices=ACTIONS, max_length=24)
#     code = models.CharField(max_length=64)

#     def is_valid(self):
#         diff = timezone.now() - self.date_created
#         if diff.seconds >= 86400:
#             return False

#         return True

#     class Meta:
#         db_table = 'dreamaway_authentication_pins'


# class App(models.Model):
#     app = models.CharField(max_length=16, unique=True)
#     secret = models.CharField(max_length=64)
#     description = models.TextField()
#     url = models.URLField()

#     def get_string(self):
#         return f'description: {self.description}\nurl: {self.url}\napp_key: {self.app} \nsecret_key: {self.secret}'

#     def __str__(self):
#         return self.get_string()

#     class Meta:
#         db_table = 'dreamaway_authentication_appkeys'
