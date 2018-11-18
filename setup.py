from setuptools import setup, find_packages

# with open('README.rst', encoding='utf8') as f:
#     long_description = f.read()

setup(
    name='dhooks',
    packages=find_packages(),
    version='1.0.6',
    description='An (a)sync wrapper for discord webhooks',
    # long_description=long_description,
    # long_description_content_type='text/x-rst',
    license='MIT',
    keywords=['discord', 'webhooks', 'discordwebhooks', 'discordhooks'],
    install_requires=['aiohttp', 'requests'],
    python_requires='>=3.5',
    project_urls={
        'Source Code': 'https://github.com/4rqm/dhooks/',
        'Issue Tracker': 'https://github.com/4rqm/dhooks/issues'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Topic :: Communications :: Chat',

    ]
)
