#!/usr/bin/env python3

import requests, urllib.request, os, ast

#34.159.77.254

API_URL = 'http://127.0.0.1:25566'
USER_KEY = 'qzuxmrLGwDs3KPKX5V5KyA=='
ADMIN_KEY = "o4S9qPk284HLuC8mx8qz2rtJNJFAX2Mnqg=="

LOCATION = os.getcwd()

print(LOCATION)

headers = {'x-access-token': USER_KEY}

version = requests.get(
    '{}/version/latest'.format(API_URL), headers=headers
)

print(version.text)

content = requests.get(
    '{}/content/0.0.1'.format(API_URL), headers=headers
)

print(content.text)

# content = ast.literal_eval(requests.get(
#     '{}/content'.format(API_URL), headers=headers
# ).text)

# for mod in content:
#     tmpUrl=API_URL + f'/packages/{version.text}/{mod}'
#     print(tmpUrl)
#     urllib.request.urlretrieve(tmpUrl, filename=LOCATION+"/"+mod)
