from textwrap import dedent

from setuptools import find_packages, setup

install_requires = [
    'bcrypt',
    'python-gnupg',
    'pyopenssl',
    'selectolax',
    'orjson',
    'httpx',
    'tqdm',
    'uvloop',
    'nest_asyncio',
]

setup(
    name='proton-api-client',
    version='0.0.5',
    python_requires='>=3.10.10',
    description='Proton Mail API',
    long_description=dedent('''
    
    ### Proton Mail API
    
    #### Examples
    
    ```python
    from proton.client import ProtonMail
    
    username, password = ..., ...
    proton = ProtonMail(username, password)
    
    passphrase = 'myPass'
    pk = 'privatekey.test123@proton.me-6fdhskjgfd7s98gdgre87gregrjdhrgd7897g898.asc'
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

    directory = proton.calendar_directory()

    version = proton.version()

    plans = proton.plans()

    calendar_directory = proton.calendar_directory()

    proton.revoke_all_sessions()
    
    ```
    '''),
    long_description_content_type='text/markdown',
    author='Trevor Hobenshield',
    author_email='trevorhobenshield@gmail.com',
    url='https://github.com/trevorhobenshield/proton-api-client',
    install_requires=install_requires,
    keywords='proton api client async search automation bot scrape mail email',
    packages=find_packages(),
    include_package_data=True,
)
