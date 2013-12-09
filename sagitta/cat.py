#!/usr/bin/env python -u
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

# pylint: disable=E1101,R0903
# E1101: Module 'x' has no 'y' member
# R0903: Too few public methods

from abc import ABCMeta, abstractmethod
from numbers import Number, Complex, Real, Rational, Integral
from sagitta.inspect import classname


# Aliases
Bool = bool  # Can not be subtyped
Int = Integral
Num = Number


Category = ABCMeta('Category', (object,), {})
TypeVariable = ABCMeta('TypeVariable', (Category,), {})


class Eq(Category):

    @abstractmethod
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not(self == other)


class Ord(Eq):

    @abstractmethod
    def __lt__(self, other):
        pass

    def __le__(self, other):
        return (self <= other)

    def __gt__(self, other):
        return not(self <= other)

    def __ge__(self, other):
        return not(self < other)


class Seq(Category):

    @abstractmethod
    def __len__(self):
        pass


class Arrow(Category):
    pass


class Monad(Category):

    @abstractmethod
    def mreturn(cls, val):
        pass

    @abstractmethod
    def __rshift__(self, f):
        pass


for (cat, sub) in [
    (Category, Number),
    (Category, TypeVariable),
    (Category, Seq),
    (Eq, Complex),
    (Ord, Real),
    (Seq, list),
    # (Seq, tuple),
    # (Seq, str),
    (Arrow, Monad),
]:
    ABCMeta.register(cat, sub)
