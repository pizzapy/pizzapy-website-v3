# app/middleware.py

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.token = self.get_token_from_request(request)
        response = self.get_response(request)
        return response

    def get_token_from_request(self, request):
        if 'code' in request.GET:
            code = request.GET['code']
            token = get_access_token(request,code)
            if not token:
                return '1dfe48423a8e298af487ffad0b27f22d'  # Use a default token or handle appropriately
        else:
            token = '1dfe48423a8e298af487ffad0b27f22d'  # Use a default token if URL parameter doesn't exist; @Devs, replace this
        return token

from app.views import get_access_token
