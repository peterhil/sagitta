#!/usr/bin/env python -u
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

import sys

if sys.version_info >= (3, 0):
    from itertools import zip_longest
else:
    from itertools import izip_longest as zip_longest


from collections import Callable
from functional import compose

from sagitta.exceptions import StrictTypeError
from sagitta.typevar import TypeVariable
from sagitta.inspect import classname


def typed(*types, **constraints):
    """
    Decorator for Haskell like function type declarations.

    The last value of types is always the type of the return value.
    Constraints can be any typeclass or Python class.
    """
    def function(fun):
        return arrow(fun, *types, **constraints)
    return function


class arrow(object):
    """
    An arrow is a function typed with Haskell like function type declaration
    and it has composition operations for arrows.

    When initialized, checks that the function is compatible with the type
    declaration.

    When called, checks that it's function is called with arguments that are
    compatible to type declaration, and the function's return value matches
    the declared type.
    """
    def __init__(self, fun, *types, **constraints):
        """
        Initialize an arrow (a typed function with composition operations).

        The last value of types is always the type of the return value.
        To specify a signature for function that returns multiple values,
        use a sequence type (a tuple or a list).

        Checks that:
        - given function is callable
        - function has the right arity (the number of arguments) for type signature

        Raises a StrictTypeError if the checks fail.
        """
        if not isinstance(fun, Callable):
            raise StrictTypeError("'{0}' object is not callable.".format(type(fun).__name__))

        self._fun = fun
        self.signature = signature(*types, **constraints)

    def __call__(self, *args, **kwargs):
        if len(list(args)) != len(self.signature.args):
            raise StrictTypeError(
                "Wrong number of arguments in '{0}' for {1}."
                "".format(args, self.signature)
            )
        args = [
            self.check(arg, typeclass)
            for arg, typeclass
            in zip_longest(args, self.signature.args)
        ]
        return self.check(
            self._fun(*args),
            self.signature.returns)

    def check(self, value, expected):
        if issubclass(expected, TypeVariable):
            if expected in self.signature.constraints:
                if not issubclass(type(value), self.signature.constraints[expected]):
                    raise StrictTypeError(
                        "Expected argument '{0}' {1} to be of type {2}."
                        "".format(value, type(value), self.signature.constraints[expected])
                    )
            else:
                self.signature.constraints[expected] = type(value)
        elif not issubclass(type(value), expected):
            raise StrictTypeError(
                "Argument '{0}' {1} is of wrong type for {3}, expected {2}."
                "".format(value, type(value), expected, self.signature)
            )
        return value

    def __rshift__(self, other):
        assert isinstance(other, type(self))
        common_types = self.signature.types[:-1]
        assert other.signature.types[:len(common_types) - 1] == common_types[:-1]

        composition = self.compose(self._fun, other._fun)

        common_types.insert(0, composition)
        common_types.append(other.signature.types[-1])
        return arrow(*common_types)

    def __lshift__(self, other):
        assert isinstance(other, type(self))
        return other.__rshift__(self)

    @staticmethod
    def compose(f1, f2):
        if not isinstance(f1, Callable):
            raise StrictTypeError("'{0}' object is not callable.".format(type(f1).__name__))
        if not isinstance(f2, Callable):
            raise StrictTypeError("'{0}' object is not callable.".format(type(f2).__name__))
        def composition(*args, **kwargs):
            return f2(f1(*args, **kwargs))
        return composition

    def __repr__(self):
        sig = ', '.join(
            [classname(cat) for cat in self.signature.types] +
            [
                '{0}={1}'.format(str(cls), classname(cat))
                for cls, cat
                in list(self.signature.constraints.items())
            ]
        )
        return "{0}({1}, {2})".format(
            classname(self),
            self._fun.__name__,
            sig
        )


class signature(object):
    """
    Haskell like function type signature.

    Can be used to compare type declarations with function arguments
    to see if they are compatible.

    Last type is always the return type.
    """
    def __init__(self, *types, **constraints):

        if len(types) < 2:
            raise TypeError("Needs at least two types: an input type and a return type.")

        self.types = list(types)
        self.constraints = dict(constraints)

    @property
    def args(self):
        return self.types[:-1]

    @property
    def returns(self):
        return self.types[-1]

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.types == other.types and self.constraints == other.constraints
        return NotImplemented

    def __hash__(self):
        hash(hash(self.types) + hash(self.constraints))

    def __repr__(self):
        return "{0}({1})".format(
            classname(self),
            ', '.join(
                [classname(cat) for cat in self.types] +
                [
                    '{0}={1}'.format(str(cls), classname(cat))
                    for (cls, cat)
                    in list(self.constraints.items())
                ]
            )
        )
