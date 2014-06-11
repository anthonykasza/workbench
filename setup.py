#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()

setup(
    name='neonx',
    version='0.1.1',
    description='Handles conversion of date from NetworkX graph to Neo4j',
    long_description=readme,
    author='SuperCowPowers LLC',
    author_email='support@supercowpowers.com',
    url='https://github.com/SuperCowPowers/workbench',
    packages=[
        'workbench',
    ],
    package_dir={'workbench': 'workbench'},
    include_package_data=True,
    install_requires=['networkx', 'requests'
    ],
    license="MIT",
    zip_safe=False,
    keywords='python, security, zerorpc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
