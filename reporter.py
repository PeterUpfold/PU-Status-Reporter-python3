

import sys
import platform
import json
import requests

BASE_URI = 'https://apps.upfold.org.uk/StatusReporter'
#BASE_URI = 'http://127.0.0.1:5001'

def get_headers(key):
    """Return a set of headers for use with requests made to the StatusReporter API."""
    version = str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)
    return {
        'User-Agent': f'PU-Status-Reporter/2.0 Python/{version} {platform.platform()}',
	'Authorization': f'Bearer {key}'
    }

def get_status(context, key):
    """Get the status of the specified context."""
    req = requests.get(BASE_URI + '/status/' + context, headers=get_headers(key))
    if req.status_code != 200:
        raise IOError(f'Getting status for context {context} failed with error code {req.status_code}')
    return req.json()

def get_contexts(key):
    """Return the JSON of all available contexts."""
    req = requests.get(BASE_URI + '/context', headers=get_headers(key))
    if req.status_code != 200:
        raise IOError(f'Getting all contexts failed with error code {req.status_code}')
    return req.json()

def get_context(context, key):
    """Check if a given context exists."""
    req = requests.get(BASE_URI + '/context/' + context, headers=get_headers(key))
    if req.status_code == 200:
        return True
    elif req.status_code == 404:
        return False
    else:
        raise IOError(f'Getting existence for {context} failed with error code {req.status_code}')

def create_context(context, key):
    """Create a new context having checked the key does not already exist."""
    headers = get_headers(key)

    data = {
        'name': context
    }

    req = requests.put(BASE_URI + '/context', headers=headers, json=data)

    assert req.status_code == 200

def set_status(context, payload, key):
    """Set the status for the specified context to the given payload."""
    data = {
        'payload': payload  
    }

    req = requests.post(BASE_URI + '/status/' + context, headers=get_headers(key), json=data)
    if req.status_code != 200:
        raise IOError(f'Setting status for context {context} failed with error code {req.status_code}')
    return req.json()