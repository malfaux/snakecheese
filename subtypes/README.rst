
Notes
=====
    - "Alpha" development status is a very optimistic classifier.
    - for flames use `deadloop's blog entry on python subtypes`_

Changelog
=========
    - 2011-01-29 adrian ilarion ciobanu <cia@mud.ro>
        + initial release 0.1.1
        + pypi-related fixups
        + minor bugfixing, documentation updates, package restructuring 0.1.18
    - 2011-01-30 adrian ilarion ciobanu <cia@mud.ro>
        + improved weaktuple's __iter__() method
        + 0.1.19 release

Description
===========

*subtypes* are python types with new or removed constraints/properties.

currently, the package includes the following subtypes:

subtypes.weaktuple
------------------

    the weaktuple is a tuple with weakened immutability.
        
    the main difference between the two is that the weaktuple's
    immutability is only concerned with the size and the underlying type 
    of each component.
                    
    in other words, tuple's immutability property can be viewed as a set of three
    constraints C = (tupleSize, tupleComponentValue, tupleComponentType) (the
    third may be somehow implicit). 
    The weaktuple's set of constraints has only two components: 
    C = (tupleSize,tupleComponentType), equivalent to "tuple has a product type" if you like.
    
    the values of weaktuple's component can be updated as long as the
    component's  type and tuple's size constraints are verified. 

    applicability: storing the arguments to a function  as a tuple for a
    later function call: while computing a set of conditions, the
    arguments may be needing updates. It's easier, clearer and
    hopefully faster to do an
    inplace tuple member update:
    
    >>> from subtypes.weaktuple import weaktuple
    >>> def f(p1,p2,p3):
    ...     print "called with:(%r,%r,%r)"%(p1,p2,p3)
    ... 
    >>> o=weaktuple([1,'abc',[(1,2),(1,3),(2,3)]])
    >>> o
    (1, 'abc', [(1, 2), (1, 3),(2, 3)])
    >>> f(*o)
    called with:(1,'abc',[(1, 2),(1, 3), (2, 3)])
    >>> if issubclass(weaktuple,tuple): o[1]='cba'
    >>> f(*o)
    called with:(1,'cba',[(1,2), (1,3), (2,3)])
    >>> 


    see `weaktuple module documentation`_ for additional information


coming up:
    - weakbool

.. _weaktuple module documentation: http://packages.python.org/subtypes/subtypes.weaktuple.html
.. _deadloop's blog entry on python subtypes: http://www.deadloop.com/2011/01/python-subtypes.html

