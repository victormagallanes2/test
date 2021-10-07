from django.contrib.auth.models import AbstractUser
from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField
# from dreamaway.tags.models import Tag
# from dreamaway.authorization.models import Role
# from dreamaway.location.models import City, ContinentalRegion, Country


class User(AbstractUser):
    email = models.EmailField(unique=True)
    #picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    #phone = PhoneNumberField(blank=True, null=False)
    # about_me = models.TextField(max_length=400, blank=True)
    # continental_region = models.ForeignKey(ContinentalRegion, on_delete=models.DO_NOTHING, blank=True, null=True)
    # country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, blank=True, null=True)
    # city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=True, null=True)
    # web_site = models.URLField(max_length=250, blank=True)
    # twitter = models.TextField(max_length=400, blank=True)
    # facebook = models.TextField(max_length=400, blank=True)
    # instagram = models.TextField(max_length=400, blank=True)
    # expert = models.ManyToManyField(Tag, blank=True)
    # interests = models.TextField(max_length=400, blank=True)
    # want_offers = models.BooleanField(default=True)
    # roles = models.ManyToManyField(Role)
    # invitation_to_expert = models.BooleanField(default=True)

    # @property
    # def avatar(self):
    #     if self.picture is None or self.picture == '':
    #         return 'https://dreamaway-01.s3.amazonaws.com/media/avatars/photo_2020-05-22_02-14-54.jpg'

    #     return self.picture.url

    # @property
    # def address(self):
    #     if self.country is None or self.city is None:
    #         return ''

    #     return f'{self.city.name} {self.country.name}'

    # @property
    # def full_name(self):
    #     return f'{self.first_name} {self.last_name}'

    # def __str__(self):
    #     return self.username

    # class Meta:
    #     db_table = 'dreamaway_users'
