from django.http import HttpResponseForbidden

class CloudflareAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for Cloudflare Access headers
        email = request.headers.get('Cf-Access-Authenticated-User-Email')
        if not email:
            return HttpResponseForbidden('Forbidden: Cloudflare Access authentication required')

        # Optionally, you can add more checks here

        return self.get_response(request)