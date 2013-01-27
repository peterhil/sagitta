#!/usr/bin/env python -u
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from sagitta.inspect import classname


class SagittaError(Exception):
    """
    Base error for the Sagitta type system.
    """
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "{0}({1})".format(classname(self), repr(self.message))

    def __str__(self):
        return str(self.message)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.__class__, self.message))


class StrictTypeError(SagittaError, TypeError):
    """
    Strict type error.
    """
