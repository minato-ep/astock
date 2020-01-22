import requests
# import re


def getPage(url, user=None, pw=None):
    if user is None and pw is None:
        return requests.get(url)
    return requests.get(url, auth=('user', 'pass'))
