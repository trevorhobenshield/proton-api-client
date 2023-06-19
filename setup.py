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
    version='0.0.0',
    python_requires='>=3.10.10',
    description='Proton Mail API',
    long_description=dedent('''
    
    ### Proton Mail API
    
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
