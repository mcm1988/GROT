import json
import codecs
import datetime
import os.path
import logging
import argparse
import Auth
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def get_rank_token():
    rank_token = Client.generate_uuid()
    return rank_token


def get_user_info():
    info = api.user_info(api.authenticated_params['_uid'])
    print("Fetched user info for: %s" % info["user"]['full_name'])
    return info


def save_user_info():
    user_info = get_user_info()
    settings_file = "files/user_info.json"
    with open(settings_file, 'w') as outfile:
        json.dump(user_info, outfile, default=to_json)


if __name__ == '__main__':
    api = Auth.process_login()
