# Create your views here.
from django import http
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

import json

from forms import SignupForm
from signup import models as signup_model

@require_http_methods(['POST'])
def signup( request ):

    form = SignupForm(request.POST)
    if not form.is_valid():
        return render_to_response('signup/error.html', {'form': form}, context_instance=RequestContext(request))

    email = form.cleaned_data['email']
    scope = form.cleaned_data['scope']
    signup_questions = request.POST.dict()
    del signup_questions['email']
    del signup_questions['csrfmiddlewaretoken']
    del signup_questions['scope']
    signup_model.create_or_update_signup(email, scope, signup_questions )
    return http.HttpResponseRedirect(reverse('signup_success'))


@csrf_exempt
def signup_ajax( request ):
    form = SignupForm(request.POST)

    if not form.is_valid():
        return http.HttpResponse(400)

    email = form.cleaned_data['email']
    scope = form.cleaned_data['scope']
    signup_questions = request.POST.dict()
    del signup_questions['email']
    del signup_questions['scope']

    signup_model.create_or_update_signup(email, scope, signup_questions )
    response = http.HttpResponse(200)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response['Access-Control-Allow-Headers'] =  '*'
    response['Access-Control-Max-Age'] = '1728000'
    return response


def success(request):
    return render_to_response(
        'signup/success.html', {},
        context_instance=RequestContext(request)
    )


def count(request, scope):
    scope = int(scope)

    context = {
        'signup_count': str(len(signup_model.get_signups(scope))),
        'scope': scope
    }

    return render_to_response(
        'signup/count.html',
        context,
        context_instance=RequestContext(request)
    )


@login_required
def export(request, scope):
    scope = int(scope)
    signups = signup_model.get_signups(scope)
    return http.HttpResponse(json.dumps(signups, cls=DjangoJSONEncoder), content_type='application/json')
