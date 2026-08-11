from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db.models import F
from .models import Redirect, RedirectType

class RedirectMiddleware:
    """
    Middleware intercepting incoming paths matching Redirect model table to perform instant 301 redirects.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        redirect_obj = Redirect.objects.filter(old_path=path).first()
        if not redirect_obj and not path.endswith('/'):
            redirect_obj = Redirect.objects.filter(old_path=path + '/').first()

        if redirect_obj:
            Redirect.objects.filter(pk=redirect_obj.pk).update(hits_count=F('hits_count') + 1)
            if redirect_obj.redirect_type == RedirectType.PERMANENT:
                return HttpResponsePermanentRedirect(redirect_obj.new_path)
            return HttpResponseRedirect(redirect_obj.new_path)

        return self.get_response(request)
