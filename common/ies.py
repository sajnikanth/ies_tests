import config
from common import Helper

import requests
import json
import base64
from requests.utils import quote

env = Helper.get_env()


def diagnostics():
    endpoint = config.hostnames[env] + 'diagnostics'
    headers = {'content-Type': 'application/json'}
    return requests.get(endpoint, headers=headers)


def edit_get(edit_by_option, payload):
    endpoint = config.hostnames[env] + 'editGet/'
    headers = {'content-Type': 'application/json'}
    if edit_by_option == 'by_url':
        url_encoded_url = quote(payload['url'], safe='')
        endpoint = endpoint + 'editByUrl?' + payload['operation'] + '&url=' + url_encoded_url
    elif edit_by_option == 'by_url_encoded_operation':
        url_encoded_url = quote(payload['url'], safe='')
        base64_encoded_operation = base64.b64encode(json.dumps(payload['operation']))
        endpoint = endpoint + 'editByUrlEncodedOperation?' +\
            'operation=' + base64_encoded_operation + '&url=' + url_encoded_url
    elif edit_by_option == 'by_data':
        url_encoded_image = quote(payload['image'])
        endpoint = endpoint + 'editByData?' + payload['operation'] + '&image=' + url_encoded_image
    else:  # edit_by_option == 'by_data_encoded_operation':
        url_encoded_image = quote(payload['image'])
        base64_encoded_operation = base64.b64encode(json.dumps(payload['operation']))
        endpoint = endpoint + 'editByDataEncodedOperation?' +\
            'operation=' + base64_encoded_operation + '&image=' + url_encoded_image
    return requests.get(endpoint, headers=headers)


def edit_post(edit_by_option, payload):
    endpoint = config.hostnames[env] + 'editPost/'
    headers = {'content-Type': 'application/json'}
    if edit_by_option == 'by_url':
        url_encoded_url = quote(payload['url'], safe='')
        endpoint = endpoint + 'editByUrl?url=' + url_encoded_url
        payload = json.dumps(payload['operation'])
    elif edit_by_option == 'by_url_encoded_operation':
        url_encoded_url = quote(payload['url'], safe='')
        base64_encoded_operation = base64.b64encode(json.dumps(payload['operation']))
        endpoint = endpoint + 'editByUrlEncodedOperation?operation=' +\
            base64_encoded_operation + '&url=' + url_encoded_url
        payload = ''
    elif edit_by_option == 'by_data':
        payload = json.dumps(payload)
        endpoint = endpoint + 'editByData/'
    else:  # edit_by_option == 'by_data_encoded_operation':
        payload = json.dumps(payload)
        endpoint = endpoint + 'editByDataEncodedOperation/'
    return requests.post(endpoint, data=payload, headers=headers)
