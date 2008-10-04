r"""
A collection of utilities easing the creation of command line scripts.

cliutils is pure Python with no dependencies.

The package provides several features that may aid the simple CLI
utility-writer. Process objects give a simple way to get output from shell
commands; the C{persistence} module provides easy access to .ini-style
configuration files; a collection of decorators eases some common patterns.

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


Persistence
===========
    There's a bit of overhead involved in finding a writable directory suitable
    for storing a config file or a persistent settings hash. The L{storage_dir}
    function removes that overhead. It accepts an optional directory name; if
    it represents an absolute path, it will be treated as such. Otherwise, it
    will be treated as a path relative to a writeable directory. On Windows,
    that directory wil be the roaming profile Application Data directory; on
    *nix, it will be the current user's home directory. If the resulting path
    doesn't exist, it will be created.

    For example, finding a path to store a persistent configuration file is as
    easy as: C{f = storage_dir('.myscript.cfg')}. Of course, it's easier still
    with the L{config} function (explained below).

    The L{config} function loads or creates a .ini-style config file at a given
    directory, using ConfigParser; however, it is an improvement in two
    respects. First, it is passed through L{storage_dir}, so locating the
    config file is easier.  Second, it returns an instance of the
    L{persistence.ConfigStorage} class, which wraps a ConfigParser instance to
    provide a dictionary-like interface. Sections and options may be accessed
    like nested dictionaries. In addition, the file is automatically saved when
    values are set.

        >>> import tempfile; filename = tempfile.mkstemp()[1]
        >>> cfg = config(filename)
        >>> cfg['sec1']['option2'] = 75
        >>> cfg['sec2']['option1'] = "Some String"
        >>> cfg['sec2']['option2'] = "Another value"
        >>> f = file(filename)
        >>> print f.read()
        [sec1]
        option2 = 75
        <BLANKLINE>
        [sec2]
        option2 = Another value
        option1 = Some String
        <BLANKLINE>
        <BLANKLINE>

    Finally, the L{db} function returns a persistent dictionary, again run
    through L{storage_dir} to make file creation and access simple. It uses
    the C{shelve} module to create or load a pickled dictionary from a given
    filename. When the dictionary is modified, the pickle is saved. This allows
    for a simple, flexible database when it's unimportant that the user be able
    to modify directly the data stored therein. For all intents and purposes,
    it may be treated as a regular dictionary in the code.

        >>> import tempfile; filename = tempfile.mkstemp()[1]
        >>> cfg = db('.test-ignore')
        >>> cfg['option1'] = 10L
        >>> cfg['option2'] = [1, 2, 3, 4, (5, 6)]
        >>> print cfg
        {'option2': [1, 2, 3, 4, (5, 6)], 'option1': 10L}

    See the C{shelve} documentation for more details. The only thing added by
    this package is the mutation of the file path by L{storage_dir}.

Decorators
==========

The L{cliargs} decorator
------------------------
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

L{redirect}
-----------
    L{redirect} is an almost trivially simple decorator factory. When
    called with a file-like object, it returns a decorator that redirects
    C{sys.stdout} to that file for the duration of the execution of the
    decorated function.

        >>> from StringIO import StringIO
        >>> logfile = StringIO()
        >>> logger = redirect(logfile)
        >>> @logger
        ... def func():
        ...     print "ABCDEFGHIJK"
        ... 
        >>> func()
        >>> logfile.seek(0)
        >>> logfile.read().strip()
        'ABCDEFGHIJK'

L{indir}
--------
    L{indir} is a decorator factory that runs the decorated function in a given
    directory, changing back to the original directory on completion.
    
        >>> import os
        >>> d = os.path.realpath('/etc')
        >>> curdir = os.path.realpath(os.curdir)
        >>> @indir(d)
        ... def whereami():
        ...     return os.path.realpath(os.curdir)
        ...
        >>> whereami() == d
        True
        >>> os.path.realpath(os.curdir) == curdir
        True

"""
__version__="0.1.3"
__all__=["sh", "Process", "cliargs", "redirect_decorator", "redirect", "indir",
         "db", "config"]

from process import sh, Process
from decorators import cliargs, logged, log_decorator, redirect, indir
from persistence import *

