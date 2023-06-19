import base64
import hashlib
import os
import time
from pathlib import Path

import bcrypt
import orjson

from .constants import SRP_LEN_BYTES


class PMHash:
    """Custom expanded version of SHA512"""

    def __init__(self, b: bytes = b''):
        self.b = b

    def update(self, b: bytes) -> None:
        self.b += b

    def digest(self) -> bytes:
        return b''.join([
            hashlib.sha512(self.b + b'\0').digest(),
            hashlib.sha512(self.b + b'\1').digest(),
            hashlib.sha512(self.b + b'\2').digest(),
            hashlib.sha512(self.b + b'\3').digest()
        ])


def pm_hash(b: bytes = b''):
    return PMHash(b)


def bcrypt_b64_encode(s: bytes) -> bytes:
    bcrypt_base64 = b'./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    std_base64chars = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    s = base64.b64encode(s)
    return s.translate(bytes.maketrans(std_base64chars, bcrypt_base64))


def hash_password(hash_class: callable, password: str, salt: bytes, modulus: bytes) -> bytes:
    salt = (salt + b'protonmail')[:16]
    salt = bcrypt_b64_encode(salt)[:22]
    hashed = bcrypt.hashpw(password, b'$2y$10$' + salt)
    return hash_class(hashed + modulus).digest()


def bytes_to_long(s: bytes) -> int:
    return int.from_bytes(s, 'little')


def long_to_bytes(n: int, nbytes: int) -> bytes:
    return n.to_bytes(nbytes, 'little')


def get_random(nbytes: int) -> int:
    return bytes_to_long(os.urandom(nbytes))


def get_random_of_length(nbytes: int) -> int:
    offset = (nbytes * 8) - 1
    return get_random(nbytes) | (1 << offset)


def custom_hash(hash_class: callable, *args) -> int:
    h = hash_class()
    for s in args:
        if s is not None:
            data = long_to_bytes(s, SRP_LEN_BYTES) if isinstance(s, int) else s
            h.update(data)
    return bytes_to_long(h.digest())


def dump(path: str, **kwargs):
    fname, data = list(kwargs.items())[0]
    out = Path(path)
    out.mkdir(exist_ok=True, parents=True)
    (out / f'{fname}_{time.time_ns()}.json').write_bytes(
        orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS))
