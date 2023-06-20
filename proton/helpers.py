import base64
import hashlib
import os
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


def bcrypt_b64encode(s: bytes) -> bytes:
    bcrypt_base64 = b'./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    std_base64chars = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    s = base64.b64encode(s)
    return s.translate(bytes.maketrans(std_base64chars, bcrypt_base64))


def hash_password(hash_class: callable, password: str, salt: bytes, modulus: bytes) -> bytes:
    salt = (salt + b'protonmail')[:16]
    salt = bcrypt_b64encode(salt)[:22]
    hashed = bcrypt.hashpw(password, b'$2y$10$' + salt)
    return hash_class(hashed + modulus).digest()


def b2l(s: bytes) -> int:
    return int.from_bytes(s, 'little')


def l2b(n: int, nbytes: int) -> bytes:
    return n.to_bytes(nbytes, 'little')


def rand(nbytes: int) -> int:
    return b2l(os.urandom(nbytes))


def randl(nbytes: int) -> int:
    offset = (nbytes * 8) - 1
    return rand(nbytes) | (1 << offset)


def hash_custom(hash_class: callable, *args) -> int:
    h = hash_class()
    for s in filter(None, args):
        h.update(l2b(s, SRP_LEN_BYTES) if isinstance(s, int) else s)
    return b2l(h.digest())


def dump(path: str, **kwargs):
    fname, data = list(kwargs.items())[0]
    out = Path(path)
    out.mkdir(exist_ok=True, parents=True)
    (out / f'{fname}.json').write_bytes(orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS))
