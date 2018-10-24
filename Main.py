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


def perform_tag_search(tag):
    rank_token = get_rank_token()
    has_more = True
    tag_results = []
    while has_more and rank_token and len(tag_results) < 60:
        results = api.tag_search(tag, rank_token, exclude_list=[t['id'] for t in tag_results])
        tag_results.extend(results.get('results', []))
        has_more = results.get('has_more')
        rank_token = results.get('rank_token')
    print(json.dumps([t['name'] for t in tag_results], indent=2))
    return tag_results


def get_user_followers(tag):
    rank_token = get_rank_token()
    has_more = True
    tag_results = []
    while has_more and rank_token and len(tag_results) < 60:
        results = api.tag_search(tag, rank_token, exclude_list=[t['id'] for t in tag_results])
        tag_results.extend(results.get('results', []))
        has_more = results.get('has_more')
        rank_token = results.get('rank_token')
    print(json.dumps([t['name'] for t in tag_results], indent=2))
    return tag_results


def get_user_followings():
    rank_token = get_rank_token()
    has_more = True
    tag_results = []
    while has_more and rank_token and len(tag_results) < 60:
        results = api.tag_search('blackpink', rank_token, exclude_list=[t['id'] for t in tag_results])
        tag_results.extend(results.get('results', []))
        has_more = results.get('has_more')
        rank_token = results.get('rank_token')
    print(json.dumps([t['name'] for t in tag_results], indent=2))
    return tag_results


if __name__ == '__main__':
    api = Auth.process_login()
    save_user_info()
    while True:
        token = get_rank_token()
        search_test_results = api.tag_search('blackpink', token)
        assert len(search_test_results.get('results', [])) > 0
        print('All ok')
        break
