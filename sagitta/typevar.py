#!/usr/bin/env python -u
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

# pylint: disable=E1101
# E1101: Module 'x' has no 'y' member

import string

from sagitta.cat import TypeVariable
from sys import modules


def set_type_variables():
    module = modules.get(__name__)

    for symbol in string.ascii_uppercase:  # pylint: disable=W0402
        typevar = type(symbol, (object,), {})  # Equivalent to: class C(object): pass

        setattr(module, symbol, typevar)
        TypeVariable.register(typevar)

set_type_variables()
