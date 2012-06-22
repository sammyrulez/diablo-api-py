# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='diablo_api_py',
    version='0.0.2',
    description='Python client for Diablo 3 web api',
    author='sammyrulez',
    url='https://github.com/sammyrulez/diablo-api-py',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    py_modules=['diablo'],
    install_requires=['requests']
)

