from django.http import JsonResponse
from rest_framework import status
from .utils import create_response

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return JsonResponse(
                create_response(
                    status=False,
                    message=str(e),
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def process_exception(self, request, exception):
        return JsonResponse(
            create_response(
                status=False,
                message=str(exception),
                data=None
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )