#!/usr/bin/env python
# encoding: utf-8
#
# pylint: disable=C0111,E0611,E1101,R0201
# C0111: Missing docstring
# E0611: No name 'x' in module 'y'
# E1101: Module 'x' has no 'y' member
# R0201: Method could be a function

import math
import pytest

from sagitta.arrow import arrow, signature, typed
from sagitta.cat import Num, Real, Int, Bool, Ord
from sagitta.typevar import A

from sagitta.exceptions import StrictTypeError
from sagitta.test import raises


class TestTypedInit(object):

    def test_init(self):
        t = arrow(Bool, A, Bool, A=Num)
        assert t._fun is Bool
        assert t.signature == signature(A, Bool, A=Num)

    @pytest.mark.parametrize('types', [
        [], [A]
    ])
    def test_less_than_two_types_raises(self, types):
        with raises(TypeError, 'Needs at least two types:'):
            args = [int] + types
            arrow(*args)

    def test_uncallable_fun_raises(self):
        uncallable = 5
        with raises(StrictTypeError, 'is not callable'):
            arrow(uncallable, A, A)


class TestTypedCall(object):
    """
    It should check argument and return types.
    """
    # ---- Functions to be typed in tests ----

    @staticmethod
    def no(x):
        return not(x)

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def argcount(*args):
        return len(args)

    # -----

    def test_one_arg_fun(self):
        ano = arrow(self.no, A, Bool)

        val = True
        assert ano(val) is not(val)
        assert type(ano(val)) is bool

    def test_two_args_fun(self):
        asum = arrow(self.add, A, A, Int)

        args = (1, 2)
        assert asum(*args) == self.add(*args)
        assert type(asum(*args)) is int

    def test_wrong_arg_count_raises(self):
        with raises(StrictTypeError, 'Wrong number of arguments in'):
            t = arrow(self.no, A, Bool)
            t('one', 'extra')  # <-- Expects only one argument

    @pytest.mark.parametrize('length', range(1, 4))
    def test_wrong_arg_types_raises(self, length):
        arglist = [Bool, Int, Real]
        misfits = [4, 0.7, 1 + 1j]

        with raises(StrictTypeError, 'is of wrong type for signature'):
            t = arrow(*[self.argcount] + arglist[:length] + [Int])
            t(*misfits[:length])

    def test_wrong_return_type_raises(self):
        with raises(StrictTypeError, 'is of wrong type for signature'):
            t = arrow(self.argcount, A, Bool)  # <- bool should be Int
            t(1)

    def test_mismatching_typevariables_raises(self):
        with raises(StrictTypeError, 'Expected argument'):
            asum = arrow(self.add, A, A, A)
            asum(3, 4.0)  # <- both should be of the same type
        with raises(StrictTypeError, 'Expected argument'):
            afloat = arrow(float, A, A)  # <- should return float
            afloat(1)

class TestArrowComposition(object):
    """
    Test arrow composition operations
    """
    def test_compose(self):
        sum_of_squares = lambda x, y: x**2 + y**2

        f = arrow(sum_of_squares, Int, Int, Int)
        g = arrow(math.sqrt, Int, Real)

        assert (f >> g)(3, 4) == 5.0

    def test_compose_left(self):
        sum_of_squares = lambda x, y: x**2 + y**2

        f = arrow(sum_of_squares, Int, Int, Int)
        g = arrow(math.sqrt, Int, Real)

        assert (g << f)(3, 4) == 5.0

class TestTypedDecorator(object):
    """
    It should work as a function decorator.
    """
    def test_function_decorator(self):

        @typed(A, A, Bool, A=Ord)
        def less_than(a, b):
            return a < b

        assert less_than(3, 7) is True
        assert less_than(7, 7) is False
        assert less_than(7, 3) is False
        assert type(less_than) is arrow
