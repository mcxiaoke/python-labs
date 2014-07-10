# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


def square(x, y):
    """


    >>> square(3,5)
    35

    >>> square(10,10)
    201

    """
    return x ** 2 + y ** 2


if __name__ == '__main__':
    import doctest
    import mth

    doctest.testmod(mth)