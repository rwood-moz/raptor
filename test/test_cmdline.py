from __future__ import absolute_import, unicode_literals

import os
from argparse import ArgumentParser, Namespace

import pytest

from raptor.cmdline import verify_options


def test_verify_options(filedir):
    args = Namespace(binary='invalid/path')
    parser = ArgumentParser()

    with pytest.raises(SystemExit):
        verify_options(parser, args)

    args.binary = os.path.join(filedir, 'fake_binary.exe')
    verify_options(parser, args)  # assert no exception
