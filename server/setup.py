#!/usr/bin/env python
import setuptools


setuptools.setup(
    name='you-should-read-server',
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/you-should-read.git',
    packages=setuptools.find_packages(),
    install_requires=['asyncpg', 'sanic'],
)
