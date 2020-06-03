from typing import List
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""


def check_apiKey(apiKey, required_scopes):
    return {'test_key': 'test_value'}


def check_basic_auth(username, password, required_scopes):
    return {'test_key': 'test_value'}


