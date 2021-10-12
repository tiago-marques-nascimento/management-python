from django.template import loader
from ..shared.alert import Alert, AlertType

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def homeView(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    template = loader.get_template('home.html')
    return HttpResponse(template.render({
        'subject': request.user.username,
        'is_logged': True
    }, request))
