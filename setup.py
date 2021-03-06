# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# single-sourcing the version
with open(path.join(here, 'bstools/_version.py')) as f:
    exec(f.read())

setup(
    name='bstools',

    # Version single-sourced from bstools/_version.py
    version=__version__,

    description='Python tools for creating a Club management dashboard for Brawl Stars',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/heyudude/Brawl-Stars-Club-Tools',

    # Author details
    author='heyudude',
    author_email='',

    # Choose your license
    license='LGPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3',
    ],

    keywords='BrawlStars',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    setup_requires=['babel'],
    install_requires=['jinja2','configparser','pybrawl>=0.0.1', 'requests>=2.19.1', 'discord-webhook', 'google-api-python-client'],

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'bstools=bstools:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/heyudude/Brawl-Stars-Club-Tools/issues',
        'Source': 'https://github.com/heyudude/Brawl-Stars-Club-Tools',
    },
)
