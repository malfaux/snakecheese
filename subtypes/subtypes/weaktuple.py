"""
weaktuple subtype
see weaktuple.__doc__
"""

#import logging
#import logging.handlers
import unittest

#lgr = logging.getLogger('dbgr')

#lgr.setLevel(logging.DEBUG)
#lgr.setLevel(logging.ERROR)
#hndl = logging.StreamHandler()
#fmt = logging.Formatter("%(message)r")
#hndl.setFormatter(fmt)
#lgr.addHandler(hndl)

#dbg = lgr.debug
#err = lgr.error


class proxytype_(object):
    """
    each tuple member is encapsulated within a proxytype_,
    having all the attribute requests (except for few) proxied through
    """
    def __init__(self,ob):
        self.ob_ = ob

    def __getattr__(self,attr):

        #leave the job of raising any AttributeError exceptions
        #to our proxied object
        #dbg("request_attr: %s"%(attr,))
        return self.__dict__.get(attr,self.__dict__['ob_'].__getattr__(attr))

    #overwrite some attributes inherited from our base
    #so we can prettyprint and fool the one who shall see the output

    def __repr__(self):
        return self.__dict__['ob_'].__repr__()
    def __str__(self):
        return self.__dict__['ob_'].__str__()



class weaktuple(tuple):
    """
    the weaktuple is a tuple with weakened immutability.
    
    the main difference between the two is that the weaktuple's immutability
    is only concerned with the size and the underlying type of each component.
    
    in other words, tuple's immutability character can be viewed as a set of three
    constraints: tuple size, tuple component type and tuple component value. the
    weaktuple's set of constraints has only two entries: tuple size and tuple
    component type, equivalent to "tuple has a product type" if you like.
    
    the values of weaktuple's component can be updated as long as the component's 
    type and tuple's size constraints are verified. 
    
    the weaktuple is not a 'hacked tuple' but a properly subclassed one. the
    tuple component update constraint is solved by adding one layer of indirection
    betweek the tuple implementation and the real object, a kind of proxy if you
    like (see impl)
    
    applicability: storing the arguments to a function  as a tuple for a
    later function call: while computing a set of conditions, the
    arguments may be needing updates. It's easier, clearer and hopefully faster to do an
    inplace tuple member update:
    
    >>> from subtypes.weaktuple import weaktuple
    >>> def f(p1,p2,p3):
    ...     print "called with: (%r,%r,%r)"%(p1,p2,p3)
    ... 
    >>> o=weaktuple([1,'abc',[(1,2),(1,3),(2,3)]])
    >>> o
    (1, 'abc', [(1, 2), (1, 3), (2, 3)])
    >>> f(*o)
    called with: (1,'abc',[(1, 2), (1, 3), (2, 3)])
    >>> if issubclass(weaktuple,tuple): o[1]='cba'
    >>> f(*o)
    called with: (1,'cba',[(1, 2), (1, 3), (2, 3)])
    >>> 
    >>> ###########################################
    ...
    >>> t1=weaktuple(range(1,4))
    #a weaktuple looks and feels like a normal tuple
    >>> t1
    (1, 2, 3)
    #and the developer gets back what he sent, not the wrapper types
    >>> map(type,t1)
    [<type 'int'>, <type 'int'>, <type 'int'>]
    >>> type(t1[1])
    <type 'int'>
    >>>
    >>>#however, you can see the real member type by calling base's __getitem__
    ...
    >>> type(tuple.__getitem__(t1,1))
    <class 'weaktuple.wrapped_int'>
    >>># when returned outside the tuple, the member is the type the developer expects
    ...# int type in this case
    >>> a=reduce(lambda x,y:x+y, t1)
    >>> a
    47
    >>> type(a)
    <type 'int'>
    >>> t1
    (1, 2, 44)
    #using a normal tuple like
    >>> t2=([1,2,44])
    >>> t2
    (1, 2, 44)
    #in relation with a weaktuple just works as expected:
    >>> t1 == t2
    True
    >>> type(t1)
    <class 'weaktuple.weaktuple'>
    >>> type(t2)
    <type 'tuple'>
    >>> 
    #the iterator returns the wrapped type, not the wrapper itself
    >>> for x in t1: print type(x)
    ... 
    <type 'int'>
    <type 'int'>
    <type 'int'>
    #although you can update the members, the tuple is still immutable
    #don't forget the subscript operator returns the wrapped type, not the wrapper
    >>> t2=weaktuple(range(1,10))
    >>> t2
    (1, 2, 3, 4, 5, 6, 7, 8, 9)
    #see the wrapped object id before update
    >>> id(t2[4])
    9925336
    #and the wrapper id
    >>> id(tuple.__getitem__(t2,4))
    11413008
    #do the update
    >>> t2[4]=666
    >>> t2
    (1, 2, 3, 4, 666, 6, 7, 8, 9)
    #the wrapped object id changes
    >>> id(t2[4])
    10658496
    #but the wrapper id remains the same
    >>> id(tuple.__getitem__(t2,4))
    11413008
    #weaktuples accept any objects
    >>> s1=weaktuple('abracadabra')
    >>> s2=weaktuple('balangabala')
    >>> s1.count('a')
    5
    >>> s2.index('l')
    2
    >>> s2 > s1
    True
    >>> m=weaktuple([
    ... 1,'python has eggs',['blah',type('TheXClas',(object,),{'cm':'pepsi-cola',})()
    ... ]])
    >>> m2=weaktuple([
    ... 1,'python has eggs',['blah',type('TheXClas',(object,),{'cm':'pepsi-cola',})()
    ... ]])
    (1, 'python has eggs', ['blah', <__main__.TheXClas object at 0x7f3743feae50>])
    >>> m2
    (1, 'python has eggs', ['blah', <__main__.TheXClas object at 0x7f3743feafd0>])
    #different TheXClas object
    >>> m==m2
    False
    
    
    
    """

    def __new__(cls,it=None):
        if it is None:
            return tuple.__new__(cls)
        #TODO: the map below is slow. we need a type registry, at least
        return tuple.__new__(
            cls,
            map(lambda each_:
                type(
                    ''.join(('wrapped_',type(each_).__name__)),
                    (proxytype_,),
                    {'_realtype':type(each_)}
                )(each_),
                it)
        )
    def __getitem__(self,i):
        return tuple.__getitem__(self,i).ob_

    def __setitem__(self,i,ob):
        """
        we're not modifying the members of tuple, but the wrapped-in values
        this way, we're not breaking the tuple's "immutable" nature. anyway ...
        the f*&^@#$ bugs are elsewhere :-(
        """

        ourtype = tuple.__getitem__(self,i)._realtype
        theirtype = type(ob)

        #class X is a subclass of class X
        #isubclass(int,int): True
        #if ( theirtype is not ourtype) and (not issubclass(theirtype,ourtype)):
        if not issubclass(theirtype,ourtype):
            raise TypeError("tuple member must be of type %s or a subclass of.\
                you gave me %s" % (ourtype,theirtype))

        tuple.__getitem__(self,i).ob_ = ob

    def __iter__(self):
        return (i.ob_ for i in tuple.__iter__(self))

    #bypass the proxy layer when needed (e.g. for calling baseclass comp
    #operators
    #TODO: you really want to make this one beloe better
    @staticmethod
    def _proxy_bypass(tup):
        """
        returns a tuple bypassing the proxies, ready for richcompare operations
        this we we support tuple(range(1,3) == weaktuple(range(1,3))
        
        since our tuple members are proxies to real objects, tests like
        the one mentioned above shouldn't fail... TODO: double-thinking needed
        """
        if not issubclass(tup.__class__,tuple): raise TypeError
        if tup.__class__ == weaktuple: return tuple(tup)
        return tup

    #tuple's comp operators don't use our __iter__()
    #so we need to bypass the proxy layer before calling them
    #TODO: need to implement this in a better and faster way
    def __eq__(self,other):
        return tuple.__eq__(self._proxy_bypass(self),self._proxy_bypass(other))
    def __ge__(self,other):
        return tuple.__ge__(self._proxy_bypass(self),self._proxy_bypass(other))
    def __gt__(self,other):
        return tuple.__gt__(self._proxy_bypass(self),self._proxy_bypass(other))

    #and rewrite this as well. this bypass will give me a heart attack...
    #for 'in' operator
    def __contains__(self, item):
        return tuple.__contains__(self._proxy_bypass(self),item)

    def count(self,item):
        return tuple.count(self._proxy_bypass(self),item)
    def index(self,item):
        return tuple.index(self._proxy_bypass(self),item)




#a quick testcase. it helped me discover 3 bugs alright!
class T_weaktuple_compare_and_update(unittest.TestCase):
    def setUp(self):
        pass

    def test_weaktuple_int_compare_with_tuple_int(self):
        t1 = tuple(range(1,10))
        t2 = weaktuple(range(1,10))
        self.assertEqual(t1,t2)

    def test_weaktuple_update_items_OK(self):
        t1 = weaktuple((4,"four",[4,3,1,2]))
        str_v = "four plus one"
        t1[1] = str_v
        self.assertEqual(t1[1],str_v)

    def test_weaktuple_update_with_different_type(self):
        def chg_member_type():
            t1 = weaktuple(("abra", "cadabra"))
            t1[1] = [1,2,3]
        self.assertRaises(TypeError,chg_member_type)


    def test_weaktuple_compare_different_type_members(self):
        t1 = weaktuple((4,"four",[4,3,1,2]))
        t2 = tuple((4,"four",[4,3,1,2]))
        self.assertTrue(t1 == t2)

    def test__FOR_IN_iterators(self):
        t1 = weaktuple((4,"four",[4,3,1,2]))
        x = 4 in t1
        self.assertTrue(4 in t1)
    def test_compare_two_weaktuples(self):
        t1 = weaktuple((4,"four",[4,3,1,2]))
        t2 = weaktuple((4,"four",[4,3,1,2]))
        t3 = weaktuple((4,"four",[4,3,1,5]))
        self.assertTrue(t1 == t2)
        self.assertFalse(t1 == t3)



#if __name__ == '__main__':
#leave zooey and enter the void to run the testcase ....$#@!#$@!#$
if __name__ == '__zooey_deschanel__':
    suite = unittest.TestLoader().loadTestsFromTestCase(
        T_weaktuple_compare_and_update)
    unittest.TextTestRunner(verbosity=2).run(suite)


