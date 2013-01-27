#!/usr/bin/env python
# encoding: utf-8

import pytest  # pylint: disable=W0611

import sagitta.typevar
import string

from sagitta.cat import TypeVariable
from sagitta.test import assert_subclass


class TestTypeVariables(object):

    def test_typevars(self):  # pylint: disable=R0201
        for symbol in string.uppercase:
            assert_subclass(getattr(sagitta.typevar, symbol), TypeVariable)
