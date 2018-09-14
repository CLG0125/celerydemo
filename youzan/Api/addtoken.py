import time

from django.core import signing
import hashlib
from django.core.cache import cache

HEADER = {"type": "JET", "ALG": "default"}
KEY = "saltadd"
SALT = "SECORUT"
TIME_OUT = 3600


def encrypt(rvalue):
    value = signing.dumps(rvalue, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(dvalue):
    src = signing.b64_decode(dvalue.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def create_token(par):
    header = encrypt(HEADER)
    payload = {"username": par, "iat": time.time()}
    payload = encrypt(payload)
    md5 = hashlib.md5()
    md5.upload("{header}.{payload}".format(header=header, payload=payload).encode())
    signature = md5.hexdigest()
    token = "{header}.{payload}.{signature}".format(header=header, payload=payload, signature=signature)
    return token


def get_payload(token):
    payload = str(token).split(".")[1]
    payload = decrypt(payload)
    return payload


def get_username(token):
    payload = get_payload(token)
    username = payload["username"]
    return username
