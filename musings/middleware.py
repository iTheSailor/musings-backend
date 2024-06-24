# middleware.py

class HttpPutParsingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PUT':
            request.PUT = request.POST
            if request.content_type.startswith('multipart/form-data'):
                request.PUT = request.POST.copy()
                for key, value in request.FILES.items():
                    request.PUT[key] = value
        response = self.get_response(request)
        return response
