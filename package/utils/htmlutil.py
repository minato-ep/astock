import requests
from bs4 import BeautifulSoup as bs
# import re


def getPage(url, user=None, pw=None):
    if user is None and pw is None:
        return requests.get(url)
    return requests.get(url, auth=('user', 'pass'))


def getSoup(r):
    return bs(r.text, features='html.parser')
