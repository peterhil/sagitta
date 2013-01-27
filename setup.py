#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under the MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import with_statement
from setuptools import setup, Command

PACKAGE_NAME = 'sagitta'
PACKAGE_VERSION = '0.0.1'
PACKAGES = ['sagitta']

with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py', '-v', 'sagitta/test'])
        raise SystemExit(errno)


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    packages=PACKAGES,
    requires=[],
    install_requires=['distribute'],
    tests_require=['pytest>=2.3.4'],
    scripts=[],

    description="""Sagitta is Haskell inspired strict runtime type system for Python.

It is suited for both object oriented and functional programming, and uses
categories of type classes, type variables, type constraints and arrows
(morphisms between categories, essentially just typed functions with
associative composition operation).

README_ at Github.

.. _README: https://github.com/peterhil/sagitta/blob/master/README.md
""",
    long_description=README_TEXT,
    author='Peter Hillerström',
    author_email='peter.hillerstrom@gmail.com',
    license='MIT License',
    url='https://github.com/peterhil/sagitta',

    classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Other/Nonlisted Topic',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass = {
        'test': PyTest
    },
)