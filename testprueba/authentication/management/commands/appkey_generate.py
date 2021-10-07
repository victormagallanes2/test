import random
import string

from django.core.management.base import BaseCommand

from dreamaway.authentication.models import App


class Command(BaseCommand):
    help = 'command for user configuration'

    def add_arguments(self, parser):
        parser.add_argument('description', nargs='+', type=str)
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        base = string.ascii_letters + string.digits
        app_key = ''.join(random.sample(base, 16))
        secret_key = ''.join(random.sample(base*2, 64))
        app = App.objects.create(
            app=app_key,
            secret=secret_key,
            description=options['description'][0],
            url=options['url'][0]
        )
        return app.get_string()
