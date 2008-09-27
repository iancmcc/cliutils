r"""
A collection of utilities easing the creation of command line scripts.

cliutils is pure Python with no dependencies.

At the moment, the module provides three disparate features: Process objects, a
command-line argument parsing decorator, a logging decoratory factory, and a
decorator factory that runs functions after changing to a given directory.

Process objects
===============
    Although it isn't very difficult to execute shell commands from a Python
    script, there are several lines of overhead in the standard pattern.
    Process objects reduce the entire pattern to a single line. In addition,
    they are more flexible; they may be piped into each other, just as regular
    processes may be on the bash command line.

        >>> Process("echo 'spam and eggs'")
        spam and eggs
        >>> s = Process("echo 'spam and eggs'").stdout
        >>> s
        'spam and eggs'
        >>> p = Process("echo 'spam and eggs'") | Process("wc -w")
        >>> p.stdout
        '3'

    For convenience, a singleton object (L{sh}) is provided that is able to
    create process objects from given attributes.

        >>> sh.echo("spam and eggs") | sh.wc("-w") | sh.cat()
        3

    Arguments passed to Process objects are split using the C{shlex} module, so
    most simple strings will work just fine. More complex arguments should be
    passed in as lists:

        >>> sh.echo(["spam", "and", "eggs"])
        spam and eggs

The L{cliargs} decorator
========================
    A common pattern for shell scripts is::
        
        def main():
            parser = make_an_option_parser()
            parser.parse(sys.argv[1:])
            do_some_stuff_with_options()

        if __name__=="__main__":
            main()

    Creation of shell scripts using C{setuptools}' C{entry_points} results in a
    similar pattern; a function is called with no arguments, and must do its
    own command-line argument parsing. This makes sense in some cases, where
    complex argument parsing is required. In simple cases, however, where
    parsing of a few arguments or keywords is required, the L{cliargs}
    decorator will be of use. It does a simple parse of C{sys.argv}, using a
    parsing algorithm based on some code in C{getopt}, and calls the decorated
    function with the results::

        @cliargs
        def myScript(anarg, anotherarg, someval="default")
            "Usage: myscript anarg anotherarg [--someval VALUE]"
            print anarg anotherarg someval

    When that function is called as a result of a command line script, such
    as::
        
        $ myscript val1 val2 --someflag somevalue 

    L{cliargs} will parse C{sys.argv} and pass the results into myScript. If
    improper arguments are passed such that a C{TypeError} is raised, the
    docstring of the function will be printed; this makes that an ideal place
    to include a usage string.

    L{cliargs} is of course limited to very simple cases. More complex argument
    parsing will require the use of the C{getopt} or C{optparse} modules.

L{log_decorator}
================
    L{log_decorator} is an almost trivially simple decorator factory. When
    called with a file-like object, it returns a decorator that redirects
    C{sys.stdout} to that file for the duration of the execution of the
    decorated function.

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

L{indir}
========
    L{indir} is a decorator factory that runs the decorated function in a given
    directory, changing back to the original directory on completion.

"""
__version__="0.1.1"
__all__=["sh", "Process", "cliargs", "log_decorator"]

from process import sh, Process
from decorators import cliargs, log_decorator, indir

