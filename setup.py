import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='dhooks',
    author='kyb3r',
    packages=find_packages(),
    version='1.0.9',
    description='An (a)sync wrapper for discord webhooks',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords=['discord', 'webhooks', 'discordwebhooks', 'discordhooks'],
    python_requires='>=3.5',
    url='https://github.com/4rqm/dhooks/',
    project_urls={
        'Issue Tracker': 'https://github.com/4rqm/dhooks/issues',
        'Documentation': 'https://dhooks.readthedocs.io/'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
