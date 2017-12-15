from setuptools import setup

setup(
    name='NBAReporter',
    packages=['NBAReporter'],
    include_package_data=True,
    install_requires=[
        'requests',
        'gtts',
        'bs4',
        'flask',
        'leveldb',
        'flask-bootstrap'
    ],
)
