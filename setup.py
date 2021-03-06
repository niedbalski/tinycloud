#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="tinycloud",
    version="0.0.1",
    author="Jorge Niedbalski R.",
    author_email="niedbalski@gmail.com",
    description="",
    packages=find_packages(),
    test_suite = 'nose.collector',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    entry_points = """
    [console_scripts]
    """
)
