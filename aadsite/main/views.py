from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

import uuid
import os
import requests
import json

def index(request):
    return HttpResponse('Hello, world. You''re at the main index. Login first <a href="/login">here</a>. Then click <a href="/main/graphcall/">here</a> to see Graph data.')

def graphcall(request):
    if 'access_token' not in request.session:
        return HttpResponseRedirect('/main/login/')

    endpoint = os.getenv('RESOURCE') + '/' + os.getenv('API_VERSION') + '/me/'
    http_headers = {'Authorization': request.session.get('access_token'),
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    output = json.dumps(graph_data)

    endpoint = os.getenv('RESOURCE') + '/' + os.getenv('API_VERSION') + '/me/memberOf'
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    output += json.dumps(graph_data)

    return HttpResponse(output)