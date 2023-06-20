"""
N    A large safe prime (N = 2q+1, where q is prime)
     All arithmetic is done modulo N.
g    A generator modulo N
k    Multiplier parameter (k = H(N, g) in SRP-6a, k = 3 for legacy SRP-6)
s    User's salt
I    Username
p    Cleartext Password
H()  One-way hash function
^    (Modular) Exponentiation
u    Random scrambling parameter
a,b  Secret ephemeral values
A,B  Public ephemeral values
x    Private key (derived from p and s)
v    Password verifier
"""

from .constants import SRP_LEN_BYTES, SALT_LEN_BYTES
from .helpers import pm_hash, b2l, hash_custom, randl, hash_password, l2b


def get_ng(n_bin: bytes, g_hex: bytes) -> tuple[int, int]:
    return b2l(n_bin), int(g_hex, 16)


def hash_k(hash_class: callable, g: int, modulus: int, width: int) -> int:
    h = hash_class()
    h.update(g.to_bytes(width, 'little'))
    h.update(modulus.to_bytes(width, 'little'))
    return b2l(h.digest())


def calc_x(hash_class: callable, salt: bytes, password: str, modulus: int) -> int:
    mod = l2b(modulus, SRP_LEN_BYTES)
    exp = hash_password(hash_class, password, salt, mod)
    return b2l(exp)


def calc_client_proof(hash_class: callable, A: int, B: int, K: bytes) -> bytes:
    h = hash_class()
    h.update(l2b(A, SRP_LEN_BYTES))
    h.update(l2b(B, SRP_LEN_BYTES))
    h.update(K)
    return h.digest()


def calc_server_proof(hash_class: callable, A: int, M: bytes, K: bytes) -> bytes:
    h = hash_class()
    h.update(l2b(A, SRP_LEN_BYTES))
    h.update(M)
    h.update(K)
    return h.digest()


class User(object):
    def __init__(self, password: str, n_bin: bytes, g_hex: bytes = b"2"):
        self.p = password
        self.hash_class = pm_hash
        self.N, self.g = get_ng(n_bin, g_hex)
        self.k = hash_k(self.hash_class, self.g, self.N, SRP_LEN_BYTES)
        self.a = randl(32)
        self.A = pow(self.g, self.a, self.N)
        self.expected_server_proof = None
        self._authenticated = False
        self.bytes_s = None
        self.v = None
        self.M = None
        self.K = None
        self.S = None
        self.B = None
        self.u = None
        self.x = None

    def authenticated(self) -> bool:
        return self._authenticated

    def get_ephemeral_secret(self) -> bytes:
        return l2b(self.a, SRP_LEN_BYTES)

    def get_session_key(self) -> bytes | None:
        return self.K if self._authenticated else None

    def get_challenge(self) -> bytes:
        return l2b(self.A, SRP_LEN_BYTES)

    def process_challenge(self, bytes_s: bytes, bytes_server_challenge: bytes) -> bytes | None:
        """ Returns M or None if SRP-6a safety check is violated """
        self.bytes_s = bytes_s
        self.B = b2l(bytes_server_challenge)
        # SRP-6a safety check
        if (self.B % self.N) == 0:
            return None
        self.u = hash_custom(self.hash_class, self.A, self.B)
        # SRP-6a safety check
        if self.u == 0:
            return None
        self.x = calc_x(self.hash_class, self.bytes_s, self.p, self.N)
        self.v = pow(self.g, self.x, self.N)
        self.S = pow((self.B - self.k * self.v), (self.a + self.u * self.x), self.N)
        self.K = l2b(self.S, SRP_LEN_BYTES)
        self.M = calc_client_proof(self.hash_class, self.A, self.B, self.K)  # noqa
        self.expected_server_proof = calc_server_proof(self.hash_class, self.A, self.M, self.K)
        return self.M

    def verify_session(self, server_proof: bytes) -> None:
        if self.expected_server_proof == server_proof:
            self._authenticated = True

    def compute_v(self, bytes_s: bytes = None) -> tuple[bytes, bytes]:
        self.bytes_s = l2b(
            randl(SALT_LEN_BYTES),
            SALT_LEN_BYTES) if bytes_s is None else bytes_s
        self.x = calc_x(self.hash_class, self.bytes_s, self.p, self.N)
        return self.bytes_s, l2b(pow(self.g, self.x, self.N), SRP_LEN_BYTES)
