from django.utils.deprecation import MiddlewareMixin
from typing import Any


class ExampleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print("Request entered the middleware",request)
        return None
    
    def process_response(self, request, response):
        print("Response is leaving the middleware",response)
        return response



