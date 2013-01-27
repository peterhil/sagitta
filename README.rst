=======
Sagitta
=======

Sagitta is a Haskell inspired strict runtime type system for Python.
The name Sagitta means ‘arrow‘ in Latin.

It uses several concepts from `category theory`_ and the Haskell type
system and is usable for both object oriented and functional programming.

Arrows and type definitions
---------------------------

Arrows_ are morphisms (for Sets, that is functions) between categories.
Essentially arrows are just typed functions between categories (with the
additional requirement of having an associative_ composition_ operation).
::

    from sagitta.arrow import typed
    from sagitta.cat import Ord, bool
    from sagitta.typevar import A

    @typed(A, A, bool, A = Ord)
    def greater_than(a, b):
        return (a > b)

Categories (typeclasses_)
-------------------------

Categories are like Haskell typeclasses_, based on abstract base classes
(abc.ABCMeta and numbers):
::

    import sagitta.cat as cat

    from cat import Category, Eq, Ord, Enum, Bounded
    from cat import Number, Complex, Real, Rational, Integral
    from cat import Arrow, Monad, Functor

Type variables
--------------

Type variables are the 'a' in Haskell function type definitions:
::

    head :: [a] -> a

Equivalent in Python with Sagitta:
::

    @typed([A], A)
    def head(lst): pass

Type constraints
----------------

Type constraints are the 'Eq a =>' in Haskell function type definitions:
::

    =/= :: Eq a => a -> a -> bool

Equivalent in Python with Sagitta:
::

    @typed(A, A, bool, A = Eq)
    def equal(x, y):
        return (x == y)

Code is at Github_.

.. _category theory: http://en.wikipedia.org/wiki/Category_theory#Categories.2C_objects.2C_and_morphisms_2
.. _Arrows: http://www.haskell.org/haskellwiki/Arrow
.. _associative: http://en.wikipedia.org/wiki/Associativity
.. _composition: http://en.wikipedia.org/wiki/Function_composition
.. _typeclasses: http://learnyouahaskell.com/types-and-typeclasses

.. _Github: https://github.com/peterhil/sagitta