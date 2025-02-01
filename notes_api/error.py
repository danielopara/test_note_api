# middleware.py
from django.http import Http404, JsonResponse
from django.urls import resolve


class WrongEndpointMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Try to resolve the URL to check if it's a valid endpoint
            resolve(request.path)
        except Http404:
            # If URL doesn't match any pattern, return custom message
            return JsonResponse(
                {"error": "Wrong endpoint, the requested resource does not exist."},
                status=404
            )
        
        response = self.get_response(request)
        return response
