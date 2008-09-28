import unittest

import os
import tempfile

from cliutils.persistence import storage_dir

class TestPersistence(unittest.TestCase):
    def test_storage_dir(self):
        mydir = tempfile.mkdtemp()
        d = storage_dir(mydir)
        self.assertEqual(mydir, d)
        self.assert_(os.path.exists(d))

        mydir = '.testing'
        d2 = storage_dir(mydir)
        config = os.path.expanduser("~/.testing")
        self.assertEqual(d2, config)
        self.assert_(os.path.exists(d2))

        os.rmdir(d)
        os.rmdir(d2)

if __name__=="__main__":
    unittest.main()
