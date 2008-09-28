import os
import shelve
from ConfigParser import ConfigParser

def storage_dir(directory=""):
    """
    Obtain a directory suitable for storing a persistent file. 

    Accepts an optional directory name. If C{directory} is an absolute path, it
    will be treated as such. Otherwise, it will be treated as a path relative
    to a writeable directory (on *nix, it's the current user's home directory.
    On Windows, it's the roaming profile Application Data directory).

    If the resulting absolute path refers to a directory that does not exist,
    it will be created.
    """
    if not os.path.isabs(directory):
        try:
            from win32com.shell import shellcon, shell
        except ImportError:
            home = os.path.expanduser("~")
        else:
            home = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        directory = os.path.join(home, directory)
    if not os.path.exists(directory): 
        os.makedirs(directory)
    return directory


def config(filename, directory=""):
    """
    Open and parse a config file C{filename} in an optional given directory
    C{directory}. 

    C{directory} will be passed through L{storage_dir}, so it may be a path
    relative to the user's home directory. If left blank, therefore, it will be
    the user's home directory itself.
    """
    directory = storage_dir(directory)
    return ConfigParser(os.path.join(directory, filename))


def db(filename, directory=""):
    """
    Create or load a pickled dictionary from C{filename} in optional
    C{directory}.

    C{directory} will be passed through L{storage_dir}, so it may be a path
    relative to the user's home directory.
    """
    directory = storage_dir(directory)
    return shelve(os.path.join(directory, filename))

