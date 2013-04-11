import json
import logging

from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

import requests

from anthropod.core import db


class Select(View):

    def get(self, request):
        return render(request, 'geo/select.html', {})

    def post(self, request):
        _id = request.POST.get('id')
        return redirect('geo.detail', _id=_id)


def child_id_json(request, _id):
    '''Return json from locust to power the typeahead widget.
    '''
    url = settings.LOCUST_URL + _id
    logger = logging.getLogger('locust.client')
    logger.debug(url)
    locust_response = requests.get(url).json()
    data = []
    for item in locust_response['response']['children']:
        item['value'] = item.pop('display_name')
        data.append(item)
    resp = HttpResponse(mimetype='application/json', status=200)
    json.dump(data, resp)
    return resp


def detail(request, _id):
    context = {'id': _id}
    spec = dict(geography_id=_id)
    context['organizations'] = db.organizations.find(spec)
    return render(request, 'geo/detail.html', context)

