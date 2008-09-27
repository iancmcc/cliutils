import unittest

import os
import sys
import tempfile
from StringIO import StringIO

from cliutils.decorators import cliargs, logged, decorator, indir

class TestDecorators(unittest.TestCase):

    def test_metadecorator(self):

        def adecorator(callable):
            def inner(*args, **kwargs):
                "Inner docstring"
                return callable(*args, **kwargs)
            return inner

        decorated_adecorator = decorator(adecorator)

        @adecorator
        def badfunc(*args, **kwargs):
            """Docstring"""
            pass

        @decorated_adecorator
        def goodfunc(*args, **kwargs):
            """Docstring"""
            pass

        # When decorators are done improperly
        self.assertNotEqual(badfunc.__name__, 'badfunc')
        self.assertNotEqual(badfunc.__doc__, 'Docstring')
        # Meta-decorated decorator
        self.assertEqual(goodfunc.__name__, 'goodfunc')
        self.assertEqual(goodfunc.__doc__, 'Docstring')

    def test_cliargs(self):
        @cliargs
        def func(*args, **kwargs): 
            """Docstring"""
            return args, kwargs
        sys.argv[:] = ['executable.py', 'a', 'b', '-b', '--cde', 'fgh', 'c']
        args, kwargs = func()
        self.assertEqual(args, ('a', 'b', 'c'))
        self.assertEqual(kwargs, {'cde':'fgh', 'b':True})

    def test_usage_failover(self):
        @cliargs
        def func(a, b, c, d=None):
            "Usage information"
            pass
        sys.argv[:] = ['executable', 'a', 'b', 'c', '--e', 'f']
        sys.stdout = StringIO()
        func()
        sys.stdout.seek(0)
        result = sys.stdout.read()
        self.assertEqual(result.strip(), "Usage information")

    def test_logged(self):
        s = StringIO()
        token = "ABCDEFG"
        @logged(s)
        def func():
            print token
        func()
        s.seek(0)
        result = s.read()
        self.assertEqual(result.strip(), token)

    def test_indir(self):
        d = os.path.realpath(tempfile.mkdtemp())
        curdir = os.path.realpath(os.curdir)
        self.assert_(d!=curdir)
        @indir(d)
        def whereami():
            return os.path.realpath(os.curdir)
        newdir = whereami()
        self.assertEqual(newdir, d)
        self.assertEqual(os.path.realpath(os.curdir), curdir)

if __name__=="__main__":
    unittest.main()

