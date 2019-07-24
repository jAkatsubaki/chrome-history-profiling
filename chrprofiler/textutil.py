import re


def getUrlDomain(url: str):
    url = url.split('://')
    url[1] = url[1].split('/')[0]
    url[1] = url[1].split(':')[0]
    return url[1]

def deleteSpecifiedWord(s):
    if 'login' in s:
        return False
    elif re.match(r'[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}', s):
        # get rid of local IP
        return False
    elif s == '':
        return False

    return True