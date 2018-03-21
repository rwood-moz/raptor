# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import, print_function

import argparse

from mozlog.commandline import add_logging_group


def create_parser(mach_interface=False):
    parser = argparse.ArgumentParser()
    add_arg = parser.add_argument

    add_arg('-t', '--test', required=True, dest="test",
            help="name of raptor test to run")
    add_arg('-b', '--browser', required=True, dest="browser",
            help="name of browser that we are testing",
            choices=['firefox', 'chrome'])
    add_arg('-e', '--executablePath', required=True, dest="browser_path",
            help="path to the browser executable that we are testing")

    add_logging_group(parser)
    return parser


def parse_args(argv=None):
    parser = create_parser()
    return parser.parse_args(argv)
