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
]

setup(
    name='proton-api-client',
    version='0.0.2',
    python_requires='>=3.10.10',
    description='Proton Mail API',
    long_description=dedent('''
    
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
    
    user_settings = proton.user_settings()
    
    mail_settings = proton.mail_settings()
    
    calendar_settings = proton.calendar_settings()
    
    timezones = proton.timezones()
    
    addresses = proton.addresses()
    
    info = proton.info()
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
