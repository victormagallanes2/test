from django.http.response import JsonResponse
from .models import App


class AppKeyValidatorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            App.objects.get(app=request.headers.get('App-Key'), secret=request.headers.get('Secret-Key'))
            return self.get_response(request)
        except App.DoesNotExist:
            return JsonResponse(data={'app': 'App no registrada'}, status=401)
