import random
from decimal import Decimal
from faker import Faker
from dreamaway.api.tests.factories import BaseModelFactory
from dreamaway.users.models import User
from dreamaway.location.models import ContinentalRegion, Country, City
from dreamaway.tags.models import Tag

fake = Faker()


class ContinentalFactory(BaseModelFactory):
    model = ContinentalRegion

    def prepare_data(self):
        return {
            'id': fake.random_int(),
            'name': fake.word(),
        }

class CountryFactory(BaseModelFactory):
    model = Country

    def prepare_data(self):
        return {
            'id': fake.random_int(),
            'name': fake.word(),
        }

class CityFactory(BaseModelFactory):
    model = City

    def prepare_data(self):
        return {
            'id': fake.random_int(),
            'name': fake.word(),
        }


class ExpertFactory(BaseModelFactory):
    model = Tag

    def prepare_data(self):
        return {
            'id': fake.random_int(),
            'name': fake.word(),
            'lvl': fake.random_int(1, 12),
        }

class UserModelFactory(BaseModelFactory):
    model = User

    def prepare_data(self):
        continental = ContinentalFactory().build_instance()
        continental.save()
        country = CountryFactory().build_instance()
        country.continentalregion = continental
        country.save()
        city = CityFactory().build_instance()
        city.country = country
        city.save()
        email = fake.email()
        return {
            'email': email,
            'username': email,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'picture': fake.word(),
            'phone': fake.phone_number()[:15],
            'about_me': fake.text(),
            'web_site': fake.domain_name(),
            'facebook': fake.domain_name(),
            'twitter': fake.domain_name(),
            'instagram': fake.domain_name(),
            'password': fake.password(),
            'continental_region': continental,
            'country': country,
            'city': city,
            'is_superuser': random.choice([True, False]),
            'invitation_to_expert': random.choice([True, False]),
        }

    def save_instance(self):
        data = self.prepare_data()
        instance = self.model(**data)
        instance.set_password(data['password'])
        instance.save()
        return instance
