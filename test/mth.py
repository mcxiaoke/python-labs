# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import logging

logging.basicConfig(level=logging.INFO, filename='log.txt')


def square(x, y):
    """


    >>> square(3,5)
    35

    >>> square(10,10)
    201

    """
    logging.info('calculate square of x, y')
    return x ** 2 + y ** 2 + 1


if __name__ == '__main__':
    print 'result is', square(13, 25)
    # import doctest
    # import mth
    #
    # doctest.testmod(mth)