from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import csrf_exempt
import jwt

User = get_user_model()

@csrf_exempt
class TokenDecodeMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.csrf_exempt = True 

    def __call__(self, request):
        try:
            token = request.headers.get('Authorization', '').split(' ')[1]
        except IndexError:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            decoded_data = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            username = decoded_data['username']
            request.user = User.objects.get(username=username)
        except jwt.DecodeError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response

