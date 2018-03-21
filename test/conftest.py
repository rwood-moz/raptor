import os
import tempfile

import pytest


@pytest.fixture
def get_binary():
    try:
        from moztest.selftest.fixtures import binary
    except ImportError:
        pytest.xfail(reason="A newer version of moztest is required")

    def inner(app):
        if app != 'firefox':
            pytest.xfail(reason="{} support not implemented".format(app))

        # TODO Remove when this is running with |mach python-test|
        os.environ['PYTHON_TEST_TMP'] = tempfile.gettempdir()
        return binary()
