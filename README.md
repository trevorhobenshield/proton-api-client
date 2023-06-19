### Proton Mail API

#### Examples

```python
from proton.client import ProtonMail

username, password = ..., ...
gpg_passphrase = ...
proton = ProtonMail(username, password, gpg_passphrase=gpg_passphrase)

# pk = 'privatekey.hotmale@proton.me-6fdhskjgfd7s98gdgre87gregrjdhrgd7897g898.asc'
# proton.gpg_import(pk)

salts = proton.salts()

users = proton.users()

inbox = proton.inbox()

conversation_id = inbox['Conversations'][0]['ID']
conversation = proton.decrypt_conversation(conversation_id)

decrypted_inbox = proton.inbox_decrypted()

core_settings = proton.user_settings()

mail_settings = proton.mail_settings()

calendar_settings = proton.calendar_settings()

timezones = proton.timezones()

addresses = proton.addresses()

info = proton.info()
```