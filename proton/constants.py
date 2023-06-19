VERSION = "0.7.1"
PM_APP_VERSION = 'web-mail@5.0.23.1'
PM_API_VERSION = 4
SRP_LEN_BYTES = 256
SALT_LEN_BYTES = 10

DEFAULT_TIMEOUT = (3.05, 27)

DEFAULT_HEADERS = {
    'authority': 'account.proton.me',
    'accept': 'application/vnd.protonmail.v1+json',
    'accept-language': 'en-GB,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://account.proton.me',
    'referer': 'https://account.proton.me',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'x-pm-appversion': PM_APP_VERSION,
    'x-pm-apiversion': f'{PM_API_VERSION}',
}

DNS_HOSTS = [
    "https://dns11.quad9.net/dns-query",
    "https://dns.google/dns-query"
]
ENCODED_URLS = [
    "dMFYGSLTQOJXXI33OOZYG4LTDNA.protonpro.xyz",
    "dMFYGSLTQOJXXI33ONVQWS3BOMNUA.protonpro.xyz"
]

PUBKEY_MAP = {
    "api.protonvpn.ch": [
        "drtmcR2kFkM8qJClsuWgUzxgBkePfRCkRpqUesyDmeE=",
        "YRGlaY0jyJ4Jw2/4M8FIftwbDIQfh8Sdro96CeEel54=",
        "AfMENBVvOS8MnISprtvyPsjKlPooqh8nMB/pvCrpJpw=",
    ],
    "protonvpn.com": [
        "8joiNBdqaYiQpKskgtkJsqRxF7zN0C0aqfi8DacknnI=",
        "JMI8yrbc6jB1FYGyyWRLFTmDNgIszrNEMGlgy972e7w=",
        "Iu44zU84EOCZ9vx/vz67/MRVrxF1IO4i4NIa8ETwiIY=",
    ],
}

ALT_MAP = {
    "backup": [
        "EU6TS9MO0L/GsDHvVc9D5fChYLNy5JdGYpJw0ccgetM=",
        "iKPIHPnDNqdkvOnTClQ8zQAIKG0XavaPkcEo0LBAABA=",
        "MSlVrBCdL0hKyczvgYVSRNm88RicyY04Q2y5qrBt0xA=",
        "C2UxW0T1Ckl9s+8cXfjXxlEqwAfPM4HiW2y3UdtBeCw="
    ]
}

SRP_MOD_KEY = """-----BEGIN PGP PUBLIC KEY BLOCK-----

xjMEXAHLgxYJKwYBBAHaRw8BAQdAFurWXXwjTemqjD7CXjXVyKf0of7n9Ctm
L8v9enkzggHNEnByb3RvbkBzcnAubW9kdWx1c8J3BBAWCgApBQJcAcuDBgsJ
BwgDAgkQNQWFxOlRjyYEFQgKAgMWAgECGQECGwMCHgEAAPGRAP9sauJsW12U
MnTQUZpsbJb53d0Wv55mZIIiJL2XulpWPQD/V6NglBd96lZKBmInSXX/kXat
Sv+y0io+LR8i2+jV+AbOOARcAcuDEgorBgEEAZdVAQUBAQdAeJHUz1c9+KfE
kSIgcBRE3WuXC4oj5a2/U3oASExGDW4DAQgHwmEEGBYIABMFAlwBy4MJEDUF
hcTpUY8mAhsMAAD/XQD8DxNI6E78meodQI+wLsrKLeHn32iLvUqJbVDhfWSU
WO4BAMcm1u02t4VKw++ttECPt+HUgPUq5pqQWe5Q2cW4TMsE
=Y4Mw
-----END PGP PUBLIC KEY BLOCK-----"""

SRP_MOD_KEY_FINGERPRINT = "248097092b458509c508dac0350585c4e9518f26"
