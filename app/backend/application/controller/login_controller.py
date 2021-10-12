from django.template import loader
from ..shared.alert import Alert, AlertType

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def loginView(request):

    template = loader.get_template('login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        else:
            context = {
                'alerts': [Alert(AlertType.ERROR, "Invalid credentials")],
                'username': username,
                'password': password
            }
            return HttpResponse(template.render(context, request))

    else:
        context = {
            'username': '',
            'password': ''
        }
        return HttpResponse(template.render(context, request))

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
