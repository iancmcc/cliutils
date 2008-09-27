import os
import sys
__all__ = ["cliargs", "logged", "log_decorator"]

def decorator(callable):
    """
    Simple meta-decorator that makes decorators preserve the attributes of the
    modified function. 

    Stolen from innumerable online recipes, but most directly from 
    U{http://wiki.python.org/moin/PythonDecoratorLibrary}.
    """
    def inner(f):
        dec = callable(f)
        dec.__name__ = f.__name__
        dec.__doc__ = f.__doc__
        dec.__module__ = f.__module__
        dec.__dict__.update(f.__dict__)
        return dec
    inner.__name__ = callable.__name__
    inner.__module__ = callable.__module__
    inner.__doc__ = callable.__doc__
    inner.__dict__.update(callable.__dict__)
    return inner

@decorator
def cliargs(callable):
    """
    Decorator that parses C{sys.argv} and passes the results into the function.

    Meant for functions that are a target of setuptools' automatic script
    creation (by default, nothing is passed in, and the function must handle
    sys.argv parsing itself). If something very simple is all that is required,
    this is the answer. Fancier arguments should use C{getopt} or C{optparse}.

    If the wrong args/kwargs are passed in such that a TypeError is raised, the
    docstring is printed, so that's an ideal place to put usage information.
    """
    def inner():
        args = sys.argv[1:]
        opts = {}
        prog_args = []
        while args:
            if args[0].startswith('-'):
                if args[1].startswith('-'):
                    opts[args[0].lstrip('-')] = True
                    args = args[1:]
                else:
                    opts[args[0].lstrip('-')] = args[1]
                    args = args[2:]
            else:
                prog_args.append(args[0])
                args = args[1:]
        try: return callable(*prog_args, **opts)
        except TypeError: print callable.__doc__
    return inner

def logged(fobj):
    """
    Factory for a decorator that redirects sys.stdout to a given file-like
    object during function execution. Thus, C{print} statements can become
    logged statements.
    """
    @decorator
    def logdecorator(callable):
        def inner(*args, **kwargs):
            stdout_backup = sys.stdout
            sys.stdout = fobj
            result = callable(*args, **kwargs)
            sys.stdout = stdout_backup
            return result
        return inner
    return logdecorator

def log_decorator(fobj):
    """
    Create a L{logged} decorator for re-use.

        >>> from StringIO import StringIO
        >>> logfile = StringIO()
        >>> logger = log_decorator(logfile)
        >>> @logger
        ... def func():
        ...     print "ABCDEFGHIJK"
        ... 
        >>> func()
        >>> logfile.seek(0)
        >>> logfile.read().strip()
        'ABCDEFGHIJK'

    """
    return logged(fobj)


def indir(newdir):
    """
    Factory for decorator that ensures the decorated function is run in a
    specified directory, then changes back to original directory.

        >>> import tempfile
        >>> realpath = os.path.realpath
        >>> new, cur = map(realpath, (tempfile.mkdtemp(), os.curdir))
        >>> @indir(new)
        ... def whereami():
        ...     return realpath(os.curdir)
        ...
        >>> whereami() == new
        True
        >>> realpath(os.curdir) == cur
        True

    """
    @decorator
    def dec(f):
        def inner(*args, **kwargs):
            olddir = os.path.abspath(os.curdir)
            os.chdir(newdir)
            result = f(*args, **kwargs)
            os.chdir(olddir)
            return result
        return inner
    return dec

