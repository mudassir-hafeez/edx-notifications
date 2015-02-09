"""
View handlers for HTML serving
"""

from django.template import RequestContext, loader
from django.http import (
    HttpResponse,
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from edx_notifications.lib.publisher import (
    register_notification_type,
    publish_notification_to_user,
)

from edx_notifications.data import (
    NotificationMessage,
    NotificationType,
)

from .forms import *


@login_required
def index(request):
    """
    Returns a basic HTML snippet rendering of a notification count
    """

    if request.method == 'POST':
        msg_type = NotificationType(
            name='testserver.type1'
        )
        register_notification_type(msg_type)

        msg = NotificationMessage(
            msg_type=msg_type,
            payload={
                'foo': 'bar'
            }
        )

        publish_notification_to_user(request.user.id, msg)

    template = loader.get_template('index.html')

    context = RequestContext(request, {'user': request.user})
    return HttpResponse(template.render(context))


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
        variables = RequestContext(
            request, {
                'form': form
            }
        )

    return render_to_response(
        'registration/register.html',
        variables,
    )

def register_success(request):
    return render_to_response(
        'registration/success.html',
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')