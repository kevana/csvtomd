"""
Tests for cvstomd.

Run with:
    $ py.test tests.py
"""

import pytest
import subprocess
from subprocess import CalledProcessError, Popen, PIPE
from tempfile import NamedTemporaryFile


def run_shell(command):
    return subprocess.check_output(command, shell=True)


def run_interactive_shell(args, input):
    p = Popen(['./csvtomd.py'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout =  p.communicate(input.encode())[0]
    returncode = p.poll()
    return stdout.decode(), returncode


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
            assert e.returncode == 2
            return
        assert False

    def test_single_row(self):
        f = make_tmpfile('1,2,3\n')
        ret = run_shell('./csvtomd.py ' + f.name).decode()
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n'

    def test_multiple_rows(self):
        f = make_tmpfile('1,2,3\n4,5,6\n')
        ret = run_shell('./csvtomd.py ' + f.name).decode()
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n4  |  5  |  6\n'

    def test_two_files(self):
        f = make_tmpfile('1,2,3\n')
        g = make_tmpfile('4,5,6\n')
        ret = run_shell('./csvtomd.py %s %s' % (f.name, g.name)).decode()
        expected = '''------------
''' + f.name + '''

1  |  2  |  3
---|-----|---

------------
''' + g.name + '''

4  |  5  |  6
---|-----|---
'''
        assert ret == expected

    def test_no_filenames_single_file(self):
        f = make_tmpfile('1,2,3\n')
        ret = run_shell('./csvtomd.py -n ' + f.name).decode()
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n'

    def test_two_files_no_filenames(self):
        f = make_tmpfile('1,2,3\n')
        g = make_tmpfile('4,5,6\n')
        ret = run_shell('./csvtomd.py %s %s' % (f.name, g.name)).decode()
        expected = '''------------
''' + f.name + '''

1  |  2  |  3
---|-----|---

------------
''' + g.name + '''

4  |  5  |  6
---|-----|---
'''
        assert ret == expected

    @pytest.mark.xfail(reason='Unimplemented feature')
    def test_mismatched_row_length(self):
        f = make_tmpfile('1,2,3\n4,5\n')
        ret = run_shell('./csvtomd.py ' + f.name).decode()
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n4  |  5  |   \n'

    def test_help(self):
        ret = run_shell('./csvtomd.py -h').decode()
        assert ret

    def test_padding(self):
        f = make_tmpfile('1,2,3\n')
        ret = run_shell('./csvtomd.py -p 0 ' + f.name).decode()
        assert ret == '------------\n1|2|3\n-|-|-\n'

    def test_padding_invalid(self):
        try:
            run_shell('./csvtomd.py -p -1')
        except CalledProcessError as e:
            assert e.returncode == 1
            return
        assert False

    def test_stdin_single_row(self):
        ret, returncode = run_interactive_shell(['-s'], '1,2,3\n')
        assert returncode == 0
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n'

    def test_stdin_multiple_rows(self):
        ret, returncode = run_interactive_shell(['-s'], '1,2,3\n4,5,6\n')
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n4  |  5  |  6\n'


    @pytest.mark.xfail(reason='Unimplemented feature')
    def test_stdin_mismatched_row_length(self):
        ret, returncode = run_interactive_shell(['-s'], '1,2,3\n4,5\n')
        assert ret == '------------\n1  |  2  |  3\n---|-----|---\n4  |  5  |  \n'

    def test_stdin_padding(self):
        ret, returncode = run_interactive_shell(['-s', '-p', '1'], '1,2,3\n')
        assert ret == '------------\n1 | 2 | 3\n--|---|--\n'

    def test_stdin_padding_invalid(self):
        ret, returncode = run_interactive_shell(['-s', '-p', '-2'], '1,2,3\n')
        assert returncode == 1

    def test_missing_file(self):
        pass

    def test_empty_file(self):
        pass

    def test_single_field(self):
        pass


