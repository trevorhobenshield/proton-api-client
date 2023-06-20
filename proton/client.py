from subprocess import Popen, PIPE

import gnupg
from selectolax.lexbor import LexborHTMLParser
from tqdm import tqdm

from .constants import PM_APP_VERSION_ACCOUNT
from .login import login


class ProtonMail:
    def __init__(self, username: str, password: str, gpg_passphrase: str = None):
        self.gpg = gnupg.GPG()
        self.gpg_passphrase = gpg_passphrase
        self.client = login(username, password)
        self.api = 'https://api.protonmail.ch/api'
        self.mail_api = 'https://mail.proton.me/api'
        self.account_api = 'https://account.proton.me/api'

    def salts(self):
        return self.client.get(f'{self.account_api}/core/v4/keys/salts').json()

    def users(self):
        return self.client.get(f'{self.account_api}/core/v4/users').json()

    def sessions(self):
        return self.client.get(f'{self.account_api}/auth/v4/sessions').json()

    def info(self):
        headers = dict(self.client.headers) | {'x-pm-appversion': PM_APP_VERSION_ACCOUNT}
        return self.client.post(f'{self.account_api}/core/v4/auth/info', headers=headers).json()

    def revoke_all_sessions(self):
        self.client.delete(f'{self.account_api}/auth/v4/sessions')

    def gpg_import(self, fname: str, passphrase: str = None):
        self.gpg.import_keys_file(fname, passphrase=passphrase or self.gpg_passphrase)

    def gpg_decrypt(self, data: str, passphrase: str = None) -> str:
        return self.gpg.decrypt(data, passphrase=passphrase or self.gpg_passphrase).data.decode()

    def gpg_clean(self) -> list[dict]:
        fingerprints = [x['fingerprint'] for x in self.gpg.list_keys()]
        options = ['--delete-secret-keys', '--delete-keys']
        res = []
        for opt in options:
            cmd = f'gpg --yes --batch {opt} {" ".join(fingerprints)}'
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
            out, err = p.communicate(input=b'y\ny\n')
            res.append({'err': err.decode(), 'out': out.decode()})
        return res

    def inbox(self, params: dict = None) -> dict:
        params = params or {
            'Page': 0,
            'PageSize': 150,  # max page size
            'LabelID': 0,
            'Sort': 'Time',
            'Desc': 1,
            # 'Limit': 100,
            # 'Attachments': 1, # only get messages with attachments
        }
        return self.client.get(f"{self.api}/mail/v4/conversations", params=params).json()

    def user_settings(self) -> dict:
        return self.client.get(f'{self.api}/core/v4/settings').json()

    def mail_settings(self) -> dict:
        return self.client.get(f'{self.api}/mail/v4/settings').json()

    def calendar_settings(self):
        return self.client.get(f'{self.api}/settings/calendar').json()

    def timezones(self):
        return self.client.get(f'{self.api}/calendar/v1/timezones').json()

    def addresses(self, params: dict = None) -> dict:
        params = params or {
            'Page': 0,
            'PageSize': 150,  # max page size
        }
        return self.client.get(f'{self.api}/core/v4/addresses', params=params).json()

    def inbox_decrypted(self, params: dict = None):
        """
        just testing things out - move into smaller and different functions
        """
        params = params or {
            'Page': 0,
            'PageSize': 150,  # max page size
            'LabelID': 0,
            'Sort': 'Time',
            'Desc': 1,
            # 'Attachments': 1,  ## filter attachments
        }
        inbox = self.client.get(f"{self.api}/mail/v4/conversations", params=params).json()
        conversation_ids = [x.get('ID') for x in inbox.get('Conversations')]

        conversations_data = []
        for cid in conversation_ids:
            conversations_data.append(self.client.get(f"{self.api}/mail/v4/conversations/{cid}").json())

        results = {}
        for conversation in tqdm(conversations_data):
            messages = filter(None, (msg.get('Body') for msg in conversation.get('Messages', [])))
            decrypted_messages = []
            for data in messages:
                msg = self.gpg_decrypt(data)
                decrypted_messages.append(msg)

            results[conversation['Conversation']['ID']] = {
                'subject': conversation['Conversation'].get('Subject'),
                'text': '\n'.join(LexborHTMLParser(x).text() for x in decrypted_messages),
                'html': decrypted_messages,  # full html body of each message
                'metadata': conversation,
            }

        return results

    def decrypt_conversation(self, conversation_id: dict) -> dict:
        conversation = self.client.get(f"{self.api}/mail/v4/conversations/{conversation_id}").json()
        messages = filter(None, (msg.get('Body') for msg in conversation.get('Messages', [])))
        return {'id': conversation_id, 'data': [self.gpg_decrypt(data) for data in messages]}
