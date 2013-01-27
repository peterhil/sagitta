#!/usr/bin/env python -u
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import print_function

from itertools import izip_longest
from sagitta.exceptions import StrictTypeError
from sagitta.typevar import TypeVariable
from sagitta.inspect import classname


class typed(object):
    """
    Haskell like function type declarations.
    Can be used as a function or a decorator.

    Checks that the function is called with compatible arguments,
    and it's return value is of the declared type when called.
    """
    def __init__(self, fun, *types, **constraints):
        """
        Initialize a typed function (≈arrow).

        The last value of types is always the type of the return value.
        To specify a signature for function that returns multiple values,
        use a sequence (tuple, list).

        Checks that:
        - given function is callable
        - function has the right arity (the number of arguments) for type signature

        Raises a StrictTypeError if the checks fail.
        """
        if not callable(fun):
            raise StrictTypeError("'{0}' object is not callable.".format(type(fun).__name__))

        self._fun = fun
        self.signature = signature(*types, **constraints)

    def __call__(self, *args, **kwargs):
        if len(list(args)) != len(self.signature.args):
            raise StrictTypeError(
                "wrong number of arguments in '{0}' for {1}."
                "".format(', '.join(args), self.signature)
            )
        args = [
            self.check(arg, typeclass)
            for arg, typeclass
            in izip_longest(args, self.signature.args)
        ]
        return self.check(self._fun(args), self.signature.returns)

    def check(self, value, expected):
        if issubclass(expected, TypeVariable):
            return value  # TODO add checks for typeclasses
        if not issubclass(type(value), expected):
            raise StrictTypeError(
                "Argument '{0}' {1} is of wrong type for {3}, expected {2}."
                "".format(value, type(value), expected, self.signature)
            )
        else:
            return value

    def __repr__(self):
        sig = u', '.join(
            [classname(cat) for cat in self.signature.types] +
            [
                '{0}={1}'.format(str(cls), classname(cat))
                for cls, cat
                in self.signature.constraints.items()
            ]
        )
        return u"{0}({1}, {2})".format(
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

        self.type = {
            'types': types,
            'constraints': constraints,
        }

    @property
    def types(self):
        return self.type['types']

    @property
    def args(self):
        return self.types[:-1]

    @property
    def returns(self):
        return self.types[-1]

    @property
    def constraints(self):
        return self.type['constraints']

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.type == other.type
        elif isinstance(other, dict):
            return self.type == other
        return NotImplemented

    def __hash__(self):
        hash(self.type)

    def __repr__(self):
        return u"{0}({1})".format(
            classname(self),
            ', '.join(
                [classname(cat) for cat in self.types] +
                [
                    '{0}={1}'.format(str(cls), classname(cat))
                    for (cls, cat)
                    in self.constraints.items()
                ]
            )
        )
