from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

import adal
import logging
import os
import uuid

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
logging.basicConfig(format=fmt, level=lvl)

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.PORT = 8000
        self.AUTHORITY_URL = os.getenv('AUTHORITY_HOST_URL', '') + '/' + os.getenv('TENANT', '')
        self.REDIRECT_URI = 'http://localhost:{}/token/'.format(self.PORT)
        self.TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                            'response_type=code&client_id={}&redirect_uri={}&' +
                            'state={}&resource={}')        
        # One-time configuration and initialization.
        logging.debug('AuthMiddleware Loaded')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        if '/login' in request.path:
            logging.debug('AuthMiddleware /login called')
            auth_state = str(uuid.uuid4())
            request.session['state'] = auth_state
            authorization_url = self.TEMPLATE_AUTHZ_URL.format(
                os.getenv('TENANT'),
                os.getenv('CLIENT_ID'),
                self.REDIRECT_URI,
                auth_state,
                os.getenv('RESOURCE'))
            return HttpResponseRedirect(authorization_url)

        if '/token' in request.path:
            logging.debug('AuthMiddleware /token called')
            code = request.GET.get('code')
            state = request.GET.get('state')
            if state != request.session['state']:
                raise ValueError('State does not match')

            auth_context = adal.AuthenticationContext(self.AUTHORITY_URL)
            token_response = auth_context.acquire_token_with_authorization_code(code, self.REDIRECT_URI, os.getenv('RESOURCE'), os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

            # It is recommended to save this to a database when using a production app.
            request.session['access_token'] = token_response['accessToken']
            return HttpResponseRedirect('/main')

        # Code to be executed for each request/response after
        # the view is called.

        return response