import asyncio
import platform
from subprocess import Popen, PIPE
from typing import List

import gnupg
from httpx import AsyncClient, Limits, Response
from tqdm.asyncio import tqdm_asyncio

from .constants import PM_APP_VERSION_ACCOUNT
from .login import login

try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        import nest_asyncio

        nest_asyncio.apply()
except:
    ...

if platform.system() != 'Windows':
    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        ...


class ProtonMail:
    def __init__(self, username: str, password: str, gpg_passphrase: str = None):
        self.gpg = gnupg.GPG()
        self.gpg_passphrase = gpg_passphrase
        self.client = login(username, password)
        self.api = 'https://api.protonmail.ch/api'
        self.mail_api = 'https://mail.proton.me/api'
        self.account_api = 'https://account.proton.me/api'
        self.assets = 'https://account.proton.me/assets'

    def inbox(self, params: dict = None) -> dict:
        params = params or {
            'Page': 0,  # todo pagination
            'PageSize': 150,  # max page size
            'LabelID': 0,
            'Sort': 'Time',
            'Desc': 1,
            # 'Limit': 100,
            # 'Attachments': 1, # only get messages with attachments
        }
        return self._get(self.api, 'mail/v4/conversations', params=params).json()

    def inbox_decrypted(self, params: dict = None) -> list[dict]:
        async def get(client: AsyncClient, _id: str) -> dict:
            r = await client.get(f'{self.api}/mail/v4/conversations/{_id}')
            conversation = r.json()
            messages = filter(None, (msg.get('Body') for msg in conversation.get('Messages', [])))
            decrypted = []
            for data in messages:
                msg = await asyncio.to_thread(self.gpg_decrypt, data)
                decrypted.append(msg)
            return {
                'id': conversation['Conversation']['ID'],
                'subject': conversation['Conversation'].get('Subject'),
                'message': decrypted,  # html
                'metadata': conversation,
            }

        async def process(ids: list[str]) -> list[dict]:
            limits = Limits(max_connections=100)
            headers, cookies = self.client.headers, self.client.cookies
            async with AsyncClient(headers=headers, cookies=cookies, limits=limits, timeout=20) as c:
                return await tqdm_asyncio.gather(*(get(c, url) for url in ids), desc="Decrypting Inbox")

        params = params or {
            'Page': 0,  # todo pagination
            'PageSize': 150,  # max page size
            'LabelID': 0,
            'Sort': 'Time',
            'Desc': 1,
            # 'Attachments': 1,  ## filter attachments
        }
        inbox = self._get(self.api, 'mail/v4/conversations', params=params).json()
        return asyncio.run(process(x['ID'] for x in inbox['Conversations']))

    def addresses(self, params: dict = None) -> dict:
        params = params or {
            'Page': 0,
            'PageSize': 150,  # max page size
        }
        return self._get(self.api, 'core/v4/addresses', params=params).json()

    def decrypt_conversation(self, conversation_id: dict) -> dict:
        conversation = self._get(self.api, f'mail/v4/conversations/{conversation_id}').json()
        messages = filter(None, (msg.get('Body') for msg in conversation.get('Messages', [])))
        return {'id': conversation_id, 'data': [self.gpg_decrypt(data) for data in messages]}

    def info(self) -> dict:
        headers = dict(self.client.headers) | {'x-pm-appversion': PM_APP_VERSION_ACCOUNT}
        return self._get(self.account_api, 'core/v4/auth/info', headers=headers).json()

    def calendar_directory(self) -> dict:
        return self._get(self.api, 'calendar/v1/directory', params={'Type': 2}).json()

    def revoke_all_sessions(self) -> dict:
        return self._get(self.account_api, 'auth/v4/sessions').json()

    def user_settings(self) -> dict:
        return self._get(self.api, 'core/v4/settings').json()

    def mail_settings(self) -> dict:
        return self._get(self.api, 'mail/v4/settings').json()

    def calendar_settings(self) -> dict:
        return self._get(self.api, 'settings/calendar').json()

    def timezones(self) -> dict:
        return self._get(self.api, 'calendar/v1/timezones').json()

    def plans(self) -> dict:
        return self._get(self.account_api, 'payments/v4/plans').json()

    def salts(self) -> dict:
        return self._get(self.account_api, 'core/v4/keys/salts').json()

    def users(self) -> dict:
        return self._get(self.account_api, 'core/v4/users').json()

    def sessions(self) -> dict:
        return self._get(self.account_api, 'auth/v4/sessions').json()

    def version(self) -> dict:
        return self._get(self.assets, 'version.json').json()

    def gpg_import(self, fname: str, passphrase: str = None) -> None:
        self.gpg.import_keys_file(fname, passphrase=passphrase or self.gpg_passphrase)

    def gpg_decrypt(self, data: str, passphrase: str = None) -> str:
        return self.gpg.decrypt(data, passphrase=passphrase or self.gpg_passphrase).data.decode()

    def _get(self, base: str, endpoint: str, **kwargs) -> Response:
        self.client.cookies.delete('Session-Id', domain='.protonmail.ch')
        return self.client.get(f'{base}/{endpoint}', **kwargs)

    def __gpg_clear(self) -> list[dict]:
        """ Delete all GPG keys """
        fingerprints = [x['fingerprint'] for x in self.gpg.list_keys()]
        options = ['--delete-secret-keys', '--delete-keys']
        res = []
        for opt in options:
            cmd = f'gpg --yes --batch {opt} {" ".join(fingerprints)}'
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
            out, err = p.communicate(input=b'y\ny\n')
            res.append({'err': err.decode(), 'out': out.decode()})
        return res
