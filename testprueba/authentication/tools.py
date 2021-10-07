import random

from .models import App, Pin


def get_url_appkey(headers):
    app = App.objects.get(app=headers.get('App-Key'), secret=headers.get('Secret-Key'))
    return app.url


def generate_pin(user, base, action, digits=8):
    code = ''.join(random.sample(base*2, digits))
    try:
        Pin.objects.get(user=user, action=action, code=code).delete()
    except Pin.DoesNotExist:
        pass

    Pin.objects.create(user=user, action=action, code=code)
    return code


def save_pin(user, code, action):
    Pin.objects.create(user=user, code=code, action=action)


def clear_pin(user, action):
    Pin.objects.filter(user=user, action=action).delete()
