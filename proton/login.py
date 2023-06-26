from base64 import b64encode, b64decode

import gnupg
from httpx import Client

from . import User
from .constants import DEFAULT_HEADERS, GREEN, RESET, RED


def login(username: str, password: str) -> Client:
    client = Client(headers=DEFAULT_HEADERS, timeout=20)
    info = client.post(f'https://api.protonmail.ch/auth/info', json={'Username': username}).json()
    verified = gnupg.GPG().decrypt(info['Modulus'])
    modulus = b64decode(verified.data.strip())
    server_challenge = b64decode(info['ServerEphemeral'])
    salt = b64decode(info['Salt'])
    user = User(password, modulus)
    client_challenge = user.get_challenge()
    client_proof = user.process_challenge(salt, server_challenge)
    auth = client.post(f'https://api.protonmail.ch/auth', json={
        'Username': username,
        'ClientEphemeral': b64encode(client_challenge).decode('utf8'),
        'ClientProof': b64encode(client_proof).decode('utf8'),
        'SRPSession': info['SRPSession'],
    }).json()

    if auth["Code"] not in {1000, 1001}:
        if auth["Code"] == 9001:
            print('CAPTCHA')
            hvt = auth["Details"]["HumanVerificationToken"]
            ## todo: open with selenium?
            # hvt = auth["Details"]["HumanVerificationToken"]
            # r = client.get(
            #     'https://api.protonmail.ch/core/v4/captcha',
            #     params={'Token': hvt},
            #     headers=DEFAULT_HEADERS | {
            #         'x-pm-human-verification-token-type': 'captcha',
            #         'x-pm-human-verification-token': hvt,
            #     }
            # )
            # Path('captcha.html').write_bytes(r.content)
        elif auth["Code"] == 12087:
            ...  # del hvt

    user.verify_session(b64decode(auth['ServerProof']))

    # todo
    print(f'{GREEN}login success{RESET}') if user.authenticated() else print(f'{RED}login failure{RESET}')

    if auth['UID']:
        client.headers.update({
            'authorization': f'Bearer {auth["AccessToken"]}',
            'x-pm-uid': auth['UID'],
        })
    client.proton_session = {
        'UID': auth['UID'],
        'AccessToken': auth['AccessToken'],
        'RefreshToken': auth['RefreshToken'],
        'PasswordMode': auth['PasswordMode'],
        'Scope': auth['Scope'].split(),
    }
    return client
