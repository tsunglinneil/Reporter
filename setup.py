#  An issue with setuptools when you want to install_requires with flask,
# you have to set version ==> 'flask>=0.12.2'

from setuptools import setup

setup(
    name='NBAReporter',
    packages=['NBAReporter'],
    include_package_data=True,
    install_requires=[
        'requests',
        'gtts',
        'bs4',
        'flask>=0.12.2',
        'leveldb',
        'flask-bootstrap',
        'gunicorn'
    ],
)
