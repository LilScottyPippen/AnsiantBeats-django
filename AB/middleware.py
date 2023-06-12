from django.shortcuts import redirect
from django.urls import reverse


class RedirectToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return redirect(reverse('index'))

        # if request.path.startswith(reverse('admin:index')):
        #     if not request.user.is_staff:
        #         return redirect(reverse('index'))

        return response
