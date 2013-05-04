#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='trollop',
    version='0.0.11',
    author='Brent Tubbs',
    author_email='brent.tubbs@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=1.2.0',
        'isodate',
    ],
    url='http://bits.btubbs.com/trollop',
    description='A Python library for working with the Trello api.',
    long_description=open('README.rst').read(),
)
