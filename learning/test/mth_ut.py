# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import unittest

import mth


class ProductTestCase(unittest.TestCase):
    def test_ints(self):
        for x in xrange(-10, 10):
            for y in xrange(-10, 10):
                p = mth.square(x, y)
                self.failUnless(p == x ** 2 + y ** 2 + 1, 'int test failed.')

    def test_floats(self):
        for x in xrange(-10, 10):
            for y in xrange(-10, 10):
                x *= 1.0
                y *= 1.0
                p = mth.square(x, y)
                self.failUnless(p == x ** 2 + y ** 2 + 1, 'float test failed.')


if __name__ == '__main__':
    unittest.main()
