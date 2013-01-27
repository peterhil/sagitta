#!/usr/bin/env python
# encoding: utf-8
#
# pylint: disable=C0111,E0611,E1101,R0201
# C0111: Missing docstring
# E0611: No name 'x' in module 'y'
# E1101: Module 'x' has no 'y' member
# R0201: Method could be a function

import pytest

from sagitta.arrow import signature, typed
from sagitta.cat import Num, Real, Int, Bool
from sagitta.typevar import A

from sagitta.exceptions import StrictTypeError
from sagitta.test import raises


class TestTypedInit(object):

    def test_init(self):
        t = typed(Bool, A, Bool, A=Num)
        assert t._fun is Bool
        assert t.signature == signature(A, Bool, A=Num)

    @pytest.mark.parametrize('types', [
        [], [A]
    ])
    def test_less_than_two_types_raises(self, types):
        with raises(TypeError, 'Needs at least two types:'):
            args = [int] + types
            typed(*args)

    def test_uncallable_fun_raises(self):
        uncallable = 5
        with raises(StrictTypeError, 'is not callable'):
            typed(uncallable, A, A)

# ---- Functions to be typed in tests ----


def no(x):
    return not(x)


def add(x, y):
    return x + y


def argcount(*args):
    return len(args)

# -----


class TestTypedCall(object):

    def test_one_arg_fun(self):
        ano = typed(no, A, Bool)

        val = True
        assert ano(val) is not(val)
        assert type(ano(val)) is bool

    def test_two_args_fun(self):
        asum = typed(sum, A, A, Int)

        args = (1, 2)
        assert asum(*args) == add(*args)
        assert type(asum(*args)) is int

    def test_wrong_arg_count_raises(self):
        with raises(StrictTypeError, 'wrong number of arguments in'):
            t = typed(no, A, Bool)
            t('one', 'extra')  # <-- Expects only one argument

    @pytest.mark.parametrize('length', range(1, 4))
    def test_wrong_arg_types_raises(self, length):
        arglist = [Bool, Int, Real]
        misfits = [4, 0.7, 1 + 1j]

        with raises(StrictTypeError, 'is of wrong type for signature'):
            t = typed(*[argcount] + arglist[:length] + [Int])
            t(*misfits[:length])

    def test_wrong_return_type_raises(self):
        with raises(StrictTypeError, 'is of wrong type for signature'):
            t = typed(argcount, A, Bool)  # <-- Bool should be Int
            t(1)
