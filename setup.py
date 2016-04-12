# -*- coding: utf-8 -*-
"""
    streamkov
    ~~~~~~~

    Packaging
"""
from setuptools import setup, find_packages


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        result = f.read().splitlines()
    return result


def get_long_description():
    with open('README.md') as f:
        result = f.read()
    return result

setup(
    name='streamkov',
    version='1.3.6',
    url='https://github.com/bhtucker/streamkov',
    author='Benson Tucker',
    author_email='bensontucker@gmail.com',
    description='Streaming Text Markov Chain App',
    long_description=get_long_description(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any'
)
