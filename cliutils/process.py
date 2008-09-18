__all__ = ['Process', 'sh', 'AlreadyExecuted', 'InvalidCommand']

import os
import shlex
from cStringIO import StringIO
from subprocess import Popen, PIPE

class AlreadyExecuted(Exception):
    """A command that doesn't exist has been called."""
class InvalidCommand(Exception):
    """A command that doesn't exist has been called."""

def _normalize(cmd):
    """
    Turn the C{cmd} into a list suitable for subprocess.

    @param cmd: The command to be split into a list
    @type cmd: str, list
    @return: The split command, or the command passed if no splitting was
    necessary
    @rtype: list
    """
    if isinstance(cmd, (str, unicode)):
        cmd = shlex.split(cmd)
    return cmd

class Process(object):
    """
    A wrapper for subprocess.Popen that allows bash-like pipe syntax and
    simplified output retrieval.

    Processes will be executed automatically when and if stdout, stderr or a
    return code are requested. This removes the necessity of calling
    C{Popen().wait()} manually, or of capturing stdout and stderr from a
    C{communicate()} call. A small change, to be sure, but it helps reduce
    overhead for a common pattern.

    One may use the C{|} operator to pipe the output of one L{Process} into
    another:

        >>> p = Process("echo 'one two three'") | Process("wc -w")
        >>> print p.stdout
        3
        
    """
    _stdin  = PIPE
    _stdout = PIPE
    _stderr = PIPE
    _retcode = None

    def __init__(self, cmd, stdin=None):
        """
        @param cmd: A string or list containing the command to be executed.
        @type cmd: str, list
        @param stdin: An optional open file object representing input to the
        process.
        @type stdin: file
        @rtype: void
        """
        self._command = _normalize(cmd)
        if stdin is not None:
            self._stdin = stdin
        self._refreshProcess()

    def __call__(self):
        """
        Shortcut to get process output.

        @return: Process output
        @rtype: str
        """
        return self.stdout

    def __or__(self, proc):
        """
        Override default C{or} comparison so that the C{|} operator will work.
        Don't call this directly.

        @return: Process with C{self}'s stdin as stdout pipe.
        @rtype: L{Process}
        """
        if self.hasExecuted or proc.hasExecuted:
            raise AlreadyExecuted("You can't pipe processes after they've been"
                                  "executed.")
        proc._stdin = self._process.stdout
        proc._refreshProcess()
        return proc

    @property
    def hasExecuted(self):
        """
        A boolean indicating whether or not the process has already run.

        @rtype: bool
        """
        return self._retcode is not None

    def _refreshProcess(self):
        if self.hasExecuted:
            raise AlreadyExecuted("")
        try: del self._process
        except AttributeError: pass
        try:
            self._process = Popen(self._command, 
                                  stdin = self._stdin,
                                  stdout = self._stdout,
                                  stderr = self._stderr)
        except OSError, e:
            raise InvalidCommand(" ".join(self._command))

    def _execute(self):
        if not self.hasExecuted:
            self._retcode = self._process.wait()

    def __str__(self):
        return self.stdout

    def __repr__(self):
        return self.stdout

    @property
    def stdout(self):
        """
        Retrieve the contents of stdout, executing the process first if
        necessary.

        @return: The process output
        @rtype: str
        """
        self._execute()
        if not hasattr(self, '_stdoutstorage'):
            self._stdoutstorage = StringIO(self._process.stdout.read().strip())
        return self._stdoutstorage.getvalue()

    @property
    def stderr(self):
        """
        Retrieve the contents of stderr, executing the process first if
        necessary.

        @rtype: str
        @return: The process error output
        """
        self._execute()
        if not hasattr(self, '_stderrstorage'):
            self._stdoutstorage = StringIO(self._process.stderr.read().strip())
        return self._stderrstorage.getvalue()

    @property
    def retcode(self):
        """
        Get the exit code of the executed process, executing the process
        first if necessary.

        @rtype: int
        @return: The exit code of the process
        """
        self._execute()
        return self._retcode
    
    @property
    def pid(self):
        """
        Get the pid of the executed process.

        @return: The process pid
        @rtype: int
        """
        self._execute()
        return self._process.pid

    def __del__(self):
        """
        Make dead sure the process has been cleaned up when garbage is
        collected.
        """
        if self.hasExecuted:
            try: os.kill(self.pid, 9)
            except: pass


class _shell(object):
    """
    Singleton class that creates Process objects for commands passed. 
    
    Not meant to be instantiated; use the C{sh} instance.

        >>> p = sh.wc("-w")
        >>> p.__class__
        <class 'cliutils.process.Process'>
        >>> p._command
        ['wc', '-w']

    """
    def __getattribute__(self, attr):
        def inner(cmd=()):
            command = [attr]
            command.extend(_normalize(cmd))
            return Process(command)
        return inner
sh = _shell()
