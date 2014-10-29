import json
import requests

from django.conf import settings


auth_headers = {
    'Authorization': 'Bearer %s' % settings.CONSTANT_CONTACT_TOKEN,
}

contacts_url = 'https://api.constantcontact.com/v2/contacts'


def _get(url, params=None):
    """Make a GET request to the Constant Contact API"""
    if not params:
        params = {}
    params['api_key'] = settings.CONSTANT_CONTACT_API_KEY
    return requests.get(url, params=params, headers=auth_headers)


def _post(url, params=None, data=None):
    """Make a POST request to the Constant Contact API"""
    if not params:
        params = {}
    params['api_key'] = settings.CONSTANT_CONTACT_API_KEY

    if not data:
        data = {}
    return requests.post(url, data=json.dumps(data), params=params,
                         headers=auth_headers)


def is_subscribed(email):
    response = _get(contacts_url, { 'email': email })
    return len(response.json()['results']) != 0


def subscribe(email, note=None):
    if is_subscribed(email):
        return True
    data = {
        'email_addresses': [{
            'email_address': email,
        }],
        'lists': [{
            'id': settings.CONSTANT_CONTACT_LIST,
        }],
        'notes': [{
            'note': note,
        }],
    }
    if note:
        data['notes'] = [{
            'note': note,
        }]
    return _post(contacts_url, data=data).status_code == 201
