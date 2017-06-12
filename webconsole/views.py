"""The view functions for the webapp"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import LoginForm
from utils.accounts import BskyUser
from django.conf import settings

import requests
import hashlib
import logging

class login(View):
    "login view for the console app"

    def get(self, request):
        request.session['has_loggedin'] = False
        state = request.GET.get('state')

        if not request.session.get('has_loggedin', False):
            form = LoginForm()
            request.session['state'] = state

            return render(request, 'webconsole/login.html', {'form': form})

        url = "https://pitangui.amazon.com/spa/skill/account-linking-status.html?vendorId=M2NOZ5XXZFVK5B#state=" \
               + state + "&access_token=" + request.session['auth_token'] + "&token_type=Bearer"

        return HttpResponseRedirect(url)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = BskyUser(form.cleaned_data['email'],
                            form.cleaned_data['password'])

            user.login()

            if user.loggedin is True:
                request.session['has_loggedin'] = True
                request.session['auth_token'] = user.token

                url = "https://pitangui.amazon.com/spa/skill/account-linking-status.html?vendorId=M2ZAY1TEQE0B7D#state=" \
                      + request.session['state'] + "&access_token=" + user.token + "&token_type=Bearer"

                return HttpResponseRedirect(url)
            else:
                # return HttpResponse('<h2>Invalid login info!</h2>', status=400)
                return render(request, "webconsole/failure.html")
        else:
            return HttpResponse('<h2>Invalid login info!</h2>', status=400)


class fb_login(View):
    print "login view for Facebook OAuth"

    def get(self, request):
        state = request.session['state']

        auth_token = request.META.get('HTTP_ACCESS')

        user_id = request.META.get('HTTP_USERID')

        params = {'input_token': auth_token, 'access_token': settings.APP_ID+'|'+settings.APP_SECRET}
        resp = requests.get(settings.FB_GRAPH_PREFIX + "/debug_token", params=params)
        logging.info('data: %s', resp.json())

        if 'error' in resp.json():
            return render(request, 'webconsole/login.html')
        # if re-verification fails
        if resp.json()['data']['app_id'] != settings.APP_ID or resp.json()['data']['user_id'] != user_id:
            return HttpResponseRedirect(reverse('uploader:login'))
        params = {'access_token': auth_token}
        resp = requests.get(settings.FB_GRAPH_PREFIX  + '/me?fields=id,name,email', params=params)

        if 'error' in resp.json():
            return render(request, 'webconsole/login.html')

        logging.info(resp.json())
        me_id = resp.json()['id']

        if 'email' not in resp.json():
            return HttpResponse(status=401)

        email = resp.json()['email']
        if len(email) > 28:
            email = email[:28]
        uname = email + '_f'
        me_id = me_id.encode('utf-8')

        m = hashlib.md5()
        m.update(me_id)
        pw = m.hexdigest()

        user = BskyUser(uname, pw)
        user.login()

        if user.loggedin:
            request.session['has_loggedin'] = True
            request.session['auth_token'] = user.token
            request.session['fb_token'] = auth_token

            resp = state+","+str(user.token)
            return HttpResponse(resp)
        else:
            return HttpResponse(status=401)
