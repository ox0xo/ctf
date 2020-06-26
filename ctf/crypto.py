import numpy as np
from PIL import Image
from mymath import ext_gcd


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


def generate_qr_code(ary, width, height):
    """
    :param ary: [[R, G, B], [R, G, B], [R, G, B]...]
    :param width:
    :param height:
    :return: show QR code image
    """
    nd_ary = np.reshape(ary, (width, height, 3)).astype(np.uint8)
    Image.fromarray(nd_ary).show()
