import os
import shelve
from ConfigParser import ConfigParser

__all__=["storage_dir", "config", "db"]

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


class _ConfigSection(object):
    """
    Wrapper that provides dictionary-like access
    """
    def __init__(self, config, name, savefunc):
        self.name = name
        self.config = config
        self.savefunc = savefunc

    def __getitem__(self, key):
        return self.config.get(self.name, key)

    def __setitem__(self, key, value):
        value = str(value)
        if not self.config.has_section(self.name):
            self.config.add_section(self.name)
        self.config.set(self.name, key, value)
        self.savefunc()

    def __str__(self):
        return str(dict(self.items()))

    def items(self):
        return zip(self.keys(), self.values())

    def keys(self):
        return self.config.options(self.name)

    def values(self):
        return [self[key] for key in self.keys()]

    def has_option(self, option):
        return option in self.keys()


class ConfigStorage(object):

    filename = ""
    _config = ConfigParser()

    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            self.load()
        else:
            self.save()

    def load(self):
        self._config.read(self.filename)

    def save(self):
        f = file(self.filename, 'w')
        self._config.write(f)
        f.close()

    def __getitem__(self, item):
        return _ConfigSection(self._config, item, self.save)

    def keys(self):
        return self._config.sections()
    sections = keys

    def has_section(self, section):
        return self._config.has_section(section)


def config(filename, directory=""):
    """
    Open and parse a config file C{filename} in an optional given directory
    C{directory}.

    C{directory} will be passed through L{storage_dir}, so it may be a path
    relative to the user's home directory. If left blank, therefore, it will be
    the user's home directory itself.
    """
    directory = storage_dir(directory)
    config = ConfigStorage(os.path.join(directory, filename))
    return config


def db(filename, directory=""):
    """
    Create or load a pickled dictionary from C{filename} in optional
    C{directory}.

    C{directory} will be passed through L{storage_dir}, so it may be a path
    relative to the user's home directory.
    """
    directory = storage_dir(directory)
    return shelve.open(os.path.join(directory, filename), writeback=True)

