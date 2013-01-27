#!/usr/bin/env python
# encoding: utf-8
#
# pylint: disable=C0111,E1101,R0201
# C0111: Missing docstring
# E1101: Module 'x' has no 'y' member
# R0201: Method could be a function

import pytest

from sagitta.cat import Category, TypeVariable, Number, Eq, Ord, Complex, Real
from sagitta.test import assert_subclass


class TestCatogeries(object):

    @pytest.mark.parametrize(['cat', 'sub'], [
        [Category, TypeVariable],
        [Category, Number],
        [Category, Eq],
        [Eq, Ord],
        [Eq, Complex],
        [Ord, Real],
    ])
    def test_categories(self, sub, cat):
        assert_subclass(sub, cat)
