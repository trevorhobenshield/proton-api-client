### Proton Mail API

#### Examples

```python
from proton.client import ProtonMail

username, password = ..., ...
proton = ProtonMail(username, password)

passphrase = 'myPass'
pk = 'privatekey.hotmale@proton.me-6fdhskjgfd7s98gdgre87gregrjdhrgd7897g898.asc'
proton.gpg_import(pk, passphrase=passphrase)


sessions = proton.sessions()

salts = proton.salts()

users = proton.users()

inbox = proton.inbox()

cid = inbox['Conversations'][0]['ID']
conversation = proton.decrypt_conversation(cid)

decrypted_inbox = proton.inbox_decrypted()

user_settings = proton.user_settings()

mail_settings = proton.mail_settings()

calendar_settings = proton.calendar_settings()

timezones = proton.timezones()

addresses = proton.addresses()

info = proton.info()

proton.revoke_all_sessions()
```