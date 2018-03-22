import os
import tempfile
from argparse import Namespace

import pytest

from raptor.raptor import Raptor


@pytest.fixture(scope='function')
def options(request):
    opts = {
        'browser': 'firefox',
        'browser_path': 'path/to/dummy/browser',
        'test': 'test_dummy',
    }

    if hasattr(request.module, 'OPTIONS'):
        opts.update(request.module.OPTIONS)
    return Namespace(**opts)


@pytest.fixture(scope='function')
def raptor(options):
    return Raptor(options)


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
