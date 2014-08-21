"""
Tests for cvstomd.

Run with:
    $ py.test tests.py
"""

import subprocess
from subprocess import CalledProcessError
from tempfile import NamedTemporaryFile


def run_shell(command):
    return subprocess.check_output(command, shell=True, stdin=subprocess.PIPE)


def make_tmpfile(contents):
    f = NamedTemporaryFile(mode='w+t')
    f.write(contents)
    f.flush()
    return f


class TestEverything:
    """
    Tests for cvstomd.
    """

    def test_base_call(self):
        try:
            ret = run_shell('./csvtomd.py')
        except CalledProcessError as e:
            assert(e.returncode == 2)
            return
        assert(False)

    def test_single_row(self):
        f = make_tmpfile('1,2,3\n')
        ret = run_shell('./csvtomd.py ' + f.name).decode()
        assert(ret == '------------\n1  |  2  |  3\n---|-----|---\n')

    def test_multiple_rows(self):
        f = make_tmpfile('1,2,3\n4,5,6\n')
        ret = run_shell('./csvtomd.py ' + f.name).decode()
        assert(ret == '------------\n1  |  2  |  3\n---|-----|---\n4  |  5  |  6\n')

    def test_two_files(self):
        f = make_tmpfile('1,2,3\n')
        g = make_tmpfile('4,5,6\n')
        ret = run_shell('./csvtomd.py %s %s' % (f.name, g.name)).decode()
        assert(True)

    def test_mismatched_row_length(self):
        pass

    def test_two_files_no_filenames(self):
        pass

    def test_help(self):
        pass

    def test_padding(self):
        pass

    def test_padding_invalid(self):
        pass

    def test_stdin_single_row(self):
        pass

    def test_stdin_multiple_rows(self):
        pass

    def test_stdin_mismatched_row_length(self):
        pass

    def test_stdin_padding(self):
        pass

    def test_stdin_padding_invalid(self):
        pass

    def test_no_filenames_single_file(self):
        pass

    def test_no_filenames_multiple_files(self):
        pass

    def test_missing_file(self):
        pass

    def test_empty_file(self):
        pass

    def test_single_field(self):
        pass


