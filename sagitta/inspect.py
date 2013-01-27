#!/usr/bin/env python -u
# encoding: utf-8
#
# Copyright (c) 2013, Peter Hillerström <peter.hillerstrom@gmail.com>
# All rights reserved. This software is licensed under MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
"""
Inspection of types, functions and objects
"""

import abc


def istype(obj):
    return type(obj) in (type, abc.ABCMeta)


def classname(obj):
    """
    Name of the object’s class as string
    """
    if istype(obj):
        return obj.__name__
    else:
        return obj.__class__.__name__


def prop_keys(obj, public=True, private=False, magic=False, globs=False, exclude=None):
    """
    Keys of object property dictionary.
    """
    exclude = exclude or []
    if globs is False:
        exclude += ['globals', 'func_globals', '__builtins__']
    keys = [prop for prop in dir(obj) if prop not in exclude]

    ismagic = lambda p: p[:2] + p[-2:] == '____'
    isprivate = lambda p: (p[0] == '_') and (p[-1] != '_')

    return [
        prop for prop in keys
        if not(ismagic(prop) or isprivate(prop)) and public
        or ismagic(prop) and magic
        or isprivate(prop) and private
    ]


def props(obj, public=True, private=False, magic=False, globs=False, exclude=None):
    """
    Object property dictionary.
    """
    return dict([
        (prop, getattr(obj, prop)) for prop
        in prop_keys(
            obj,
            public=public, private=private, magic=magic,
            globs=globs, exclude=exclude or []
        )
    ])
