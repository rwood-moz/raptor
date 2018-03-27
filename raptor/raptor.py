#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import json
import os
import sys

from mozlog import commandline, get_default_logger
from mozprofile import create_profile

from raptor.browser import start_browser
from raptor.cmdline import parse_args
from raptor.control_server import RaptorControlServer
from raptor.gen_test_url import gen_test_url
from raptor.webext import install_webext

here = os.path.abspath(os.path.dirname(__file__))


class Raptor(object):
    """Container class for Raptor"""

    def __init__(self, app, binary):
        self.raptor_venv = os.path.join(os.getcwd(), 'raptor-venv')
        self.log = get_default_logger(component='raptor')

        self.control_server = None
        self.app = app
        self.binary = binary

        pref_file = os.path.join(here, 'preferences', '{}.json'.format(self.app))
        prefs = {}
        if os.path.isfile(pref_file):
            with open(pref_file, 'r') as fh:
                prefs = json.load(fh)

        try:
            self.profile = create_profile(self.app, preferences=prefs)
        except NotImplementedError:
            self.profile = None

    def start_control_server(self):
        self.control_server = RaptorControlServer()
        self.control_server.start()

    def run_test(self, test):
        gen_test_url(self.app, test)
        install_webext(self.app, self.profile)
        start_browser(self.app, self.binary, self.profile)

    def process_results(self):
        self.log.info('todo: process results and dump in PERFHERDER_JSON blob')
        self.log.info('- or - do we want the control server to do that?')

    def clean_up(self):
        self.control_server.stop()

        if self.profile:
            self.log.info("deleting browser profile")
            del self.profile

        self.log.info("done")


def main(args=sys.argv[1:]):
    args = parse_args()
    commandline.setup_logging('raptor', args, {'tbpl': sys.stdout})

    raptor = Raptor(args.app, args.binary)
    raptor.start_control_server()
    raptor.run_test(args.test)
    raptor.process_results()
    raptor.clean_up()


if __name__ == "__main__":
    main()
