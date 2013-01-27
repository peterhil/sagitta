#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager


def assert_subclass(sub, cat):
    msg = "Type '{0}' should{2} be a subclass of '{1}'."
    assert issubclass(sub, cat), msg.format(sub, cat, '')
    assert not issubclass(cat, sub), msg.format(cat, sub, ' not')


@contextmanager
def raises(ExpectedException, message=''):
    try:
        yield
        raise AssertionError("Did not raise expected exception {0}!".format(
            repr(ExpectedException.__name__)
        ))
    except ExpectedException as err:
        if message and message not in str(err):
            raise AssertionError('expected message "{0}" not in "{1}"'.format(
                message, str(err)
            ))
    except AssertionError:
        raise
    except Exception as err:
        raise AssertionError("Expected exception {0}, not\n\t{1}.".format(
            repr(ExpectedException.__name__), repr(err)
        ))
