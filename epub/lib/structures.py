# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
from .compat import OrderedDict, iterbytes, iteritems

class OrderedSet:
    """
    A set which keeps the ordering of the inserted items.
    Currently backs onto OrderedDict.
    """

    def __init__(self, iterable=None):
        self.dict = OrderedDict.fromkeys(iterable or ())

    def add(self, item):
        self.dict[item] = None

    def remove(self, item):
        del self.dict[item]

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def __iter__(self):
        return iter(self.dict)

    def __contains__(self, item):
        return item in self.dict

    def __bool__(self):
        return bool(self.dict)

    def __len__(self):
        return len(self.dict)


class ObjDict(dict):
    """ A dictionary that provides attribute-style access.
    """

    # only called if k not found in normal places
    def __getattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    def toDict(self):
        return to_dict(self)

    @property
    def __dict__(self):
        return self.toDict()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, dict.__repr__(self))

    def __dir__(self):
        return list(iterkeys(self))

    __members__ = __dir__  # for python2.x compatibility

    @classmethod
    def fromDict(cls, d):
        return to_dict(d, cls)

    def copy(self):
        return type(self).fromDict(self)


class ObjDict2(ObjDict):
    """
    A Class that returns a user-specified value for missing keys.
    """

    def __init__(self, *args, **kwargs):
        # Mimic collections.defaultdict constructor
        if args:
            default = args[0]
            args = args[1:]
        else:
            default = None
        super(ObjDict2, self).__init__(*args, **kwargs)
        self.__default__ = default

    def __getattr__(self, k):
        """ Gets key if it exists, otherwise returns the default value."""
        try:
            return super(ObjDict2, self).__getattr__(k)
        except AttributeError:
            return self.__default__

    def __setattr__(self, k, v):
        if k == '__default__':
            object.__setattr__(self, k, v)
        else:
            return super(ObjDict2, self).__setattr__(k, v)

    def __getitem__(self, k):
        """ Gets key if it exists, otherwise returns the default value."""
        try:
            return super(ObjDict2, self).__getitem__(k)
        except KeyError:
            return self.__default__

    @classmethod
    def fromDict(cls, d, default=None):
        # pylint: disable=arguments-differ
        return toobj(d, factory=lambda d_: cls(default, d_))

    def copy(self):
        return type(self).fromDict(self, default=self.__default__)

    def __repr__(self):
        return '{0}({1!r}, {2})'.format(
            type(self).__name__, self.__undefined__, dict.__repr__(self))


def to_obj(x, factory=ObjDict):
    """ Recursively transforms a dictionary into a ObjDict via copy.
    """
    if isinstance(x, dict):
        return factory((k, to_obj(v, factory)) for k, v in iteritems(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(to_obj(v, factory) for v in x)
    else:
        return x


def to_dict(x):
    """ Recursively converts a ObjDict into a dictionary.
    """
    if isinstance(x, dict):
        return dict((k, to_dict(v)) for k, v in iteritems(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(to_dict(v) for v in x)
    else:
        return x

if __name__ == '__main__':
    d = {
        'a': 123,
        'b': 'hello',
        'c': [5,6,7],
        'd': {
            'k1': 'v1',
            'k2': ['a', 'b', 'c']
        },
        'e': set()
    }
    o = to_obj(d)
    assert o.a == 123
    assert o.b == 'hello'
    assert o.c == [5,6,7]
    assert o.d.k1 == 'v1'
    assert o.e == set()
    # assert o.f
    print((o.c)[1])