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

from sagitta.cat import Seq
from sagitta.exceptions import StrictTypeError
from sagitta.inspect import classname, istype
from sagitta.typevar import TypeVariable


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
                "wrong number of arguments in '{0}' for {1}."
                "".format(', '.join(args), self.signature)
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

        # handle instances
        if not istype(expected):
            # TODO handle lists, tuples, arrays custom sequences separately?
            if isinstance(expected, Seq) and isinstance(value, Seq):
                return self.check_sequence(value, expected)

            raise NotImplementedError(
                "Expected value {0} {1} to match type definition:\n\t{2}, of category {3}\n\t"
                "-- if the value is of the defined type, please register it as such with a suitable\n\t"
                "type class category, for example: ABCMeta.register(Seq, {4})"
                "".format(value, type(value), expected, type(expected), classname(type(expected)))
            )
        else:
            return self.check_scalar(value, expected)


    def check_scalar(self, value, expected):
        assert istype(expected), "Expected {0} to be a type class.".format(expected)

        if issubclass(expected, TypeVariable):
            return value  # TODO add checks for typeclasses

        if issubclass(type(value), expected):
            return value

        raise StrictTypeError(
            "Argument '{0}' {1} is of wrong type for {3}, expected {2}."
            "".format(value, type(value), expected, self.signature)
        )

    def check_sequence(self, seq, expected):
        assert isinstance(expected, Seq) and isinstance(value, Seq)
        return [
            self.check(value, expected)
            for value in seq
        ]

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
        return NotImplemented

    def __hash__(self):
        hash(self.type)

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
