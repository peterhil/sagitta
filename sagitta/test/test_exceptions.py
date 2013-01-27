#!/usr/bin/env python
# encoding: utf-8
#
# pylint: disable=C0111,R0201
# C0111: Missing docstring
# R0201: Method could be a function

import pytest  # pylint: disable=W0611

from sagitta.exceptions import SagittaError, StrictTypeError


class TestSagittaError(object):

    def test_str(self):
        ex = SagittaError('you should\'ve taken the blue pill.')
        assert str(ex) == ex.message

    def test_repr(self):
        ex = SagittaError('deeper down the rabbithole.')
        assert eval(repr(ex)) == ex


class TestStrictTypeError(object):

    def test_inheritance(self):
        ex = StrictTypeError('it\'s turtles all the way down.')
        assert isinstance(ex, SagittaError)
        assert isinstance(ex, TypeError)
