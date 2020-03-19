#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='collab',
    version='0.0',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'numpy',
        'scipy'
    ]
)
