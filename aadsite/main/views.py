from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

import uuid
import adal
import config
import requests
import logging

PORT = 8000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://localhost:{}/main/token/'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
logging.basicConfig(format=fmt, level=lvl)

def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def auth(request):
    login_url = 'http://localhost:{}/main/login/'.format(PORT)
    return HttpResponseRedirect(login_url)

def login(request):
    auth_state = str(uuid.uuid4())
    request.session['state'] = auth_state
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    return HttpResponseRedirect(authorization_url)

def token(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if state != request.session['state']:
        raise ValueError("State does not match")

    auth_context = adal.AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, config.RESOURCE, config.CLIENT_ID, config.CLIENT_SECRET)

    # It is recommended to save this to a database when using a production app.
    request.session['access_token'] = token_response['accessToken']
    logging.debug('token: ' + token_response['accessToken'])
    return HttpResponseRedirect('/main/graphcall/')

def graphcall(request):
    if 'access_token' not in request.session:
        return HttpResponseRedirect('/main/login/')

    endpoint = config.RESOURCE + '/' + config.API_VERSION + '/me/'
    http_headers = {'Authorization': request.session.get('access_token'),
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    output = '<table>'
    output += '<tr><td>Key</td><td>Value</td></tr>'
    for key, value in graph_data.items():
        if (not isinstance(key, type(None)) and not isinstance(value, type(None))): 
            if (isinstance(value, list)):
                for item in value:
                    output += '<tr><td>' + key + '</td><td>' + item + '</td></tr>'
            else: 
                output += '<tr><td>' + key + '</td><td>' + value + '</td></tr>'

    output += "</table>"
    return HttpResponse(output)