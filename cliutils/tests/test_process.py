import unittest
from cliutils.process import Process, sh, InvalidCommand

class TestProcess(unittest.TestCase):

    def test_getOutput(self):
        p = Process('echo "blah"')
        self.assertEqual(p.stdout, "blah")

    def test_splitting(self):
        p = Process('echo "blah blah"')
        self.assertEqual(p.stdout, "blah blah")

    def test_shell(self):
        p = sh.echo("blah blah")
        self.assertEqual(p.stdout, "blah blah")

    def test_pipe(self):
        p = sh.echo("blah blah") | sh.wc("-w") | sh.cat()
        self.assertEqual(p.stdout, "2")

    def test_rc(self):
        p = sh.true()
        self.assertEqual(p.retcode, 0)
        p = sh.false()
        self.assertEqual(p.retcode, 1)

    def test_pid(self):
        p = sh.true()
        self.assert_(p.pid>0)

    def test_raises(self):
        self.assertRaises(InvalidCommand, sh.notacommand)

    def test_stdout_again(self):
        p = sh.echo("blah blah")
        dummy = p.stdout
        # Access it again
        self.assertEqual(p.stdout, "blah blah")


if __name__=="__main__":
    unittest.main()
