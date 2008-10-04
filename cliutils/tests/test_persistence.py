import unittest

import os
import tempfile

from cliutils.persistence import storage_dir, ConfigStorage

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

    def test_config(self):
        filename = tempfile.mkstemp()[1]
        config = ConfigStorage(filename)

        self.assertEqual(config.sections(), [])

        config['sec1']['option2'] = 75

        self.assertEqual(open(filename).read().strip(), "[sec1]\noption2 = 75")

        config2 = ConfigStorage(filename)
        self.assertEqual(config2.keys(), ['sec1'])
        self.assertEqual(config2['sec1'].items(), [('option2', '75'),])


if __name__=="__main__":
    unittest.main()
