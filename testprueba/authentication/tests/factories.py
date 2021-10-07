import random
import string
from faker import Faker
from dreamaway.api.tests.factories import BaseModelFactory
from dreamaway.authentication.models import App


fake = Faker()


class AppModelFactory(BaseModelFactory):
    model = App
    
    def prepare_data(self):
        base = string.ascii_letters + string.digits
        return {
            'app': ''.join(random.sample(base, 16)),
            'secret': ''.join(random.sample(base*2, 64)),
            'description': fake.text(),
            'url': fake.url(),
        }
