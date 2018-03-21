#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import os
import sys

from mozlog import commandline, get_default_logger

from raptor.browser import start_browser
from raptor.browser_preferences import set_browser_prefs
from raptor.cmdline import parse_args
from raptor.control_server import RaptorControlServer
from raptor.gen_test_url import gen_test_url
from raptor.profile import create_profile
from raptor.webext import install_webext


class Raptor(object):
    """Container class for Raptor"""

    def __init__(self, options):
        self.raptor_venv = os.path.join(os.getcwd(), 'raptor-venv')
        self.log = get_default_logger(component='raptor')
        self.control_server = None
        self.profile = None
        self.browser = options.browser
        self.browser_path = options.browser_path
        self.test = options.test
        self.sysdir = os.path.abspath(os.getcwd())

    def verify_options(self):
        self.log.info("TODO: Ensure cmd line options are valid before continuing i.e. test exists")

    def create_profile(self):
        self.profile = create_profile(self.browser)

    def set_browser_prefs(self):
        set_browser_prefs(self.browser, self.profile)

    def gen_test_url(self):
        gen_test_url(self.browser, self.test, self.sysdir)

    def install_webext(self):
        install_webext(self.browser, self.profile)

    def start_control_server(self):
        self.control_server = RaptorControlServer()
        self.control_server.start()

    def run_test(self):
        start_browser(self.browser, self.browser_path, self.profile)

    def process_results(self):
        self.log.info('todo: process results and dump in PERFHERDER_JSON blob')
        self.log.info('- or - do we want the control server to do that?')

    def clean_up(self):
        self.control_server.stop()
        self.log.info("deleting browser profile")
        del self.profile
        self.log.info("done")


def main(args=sys.argv[1:]):
    args = parse_args()
    commandline.setup_logging('raptor', args, {'tbpl': sys.stdout})

    raptor = Raptor(options=args)

    raptor.verify_options()
    raptor.create_profile()
    raptor.set_browser_prefs()
    raptor.gen_test_url()

    # on firefox we install the ext first; on chrome it's on cmd line
    if args.browser == 'firefox':
        raptor.install_webext()

    raptor.start_control_server()
    raptor.run_test()
    raptor.process_results()
    raptor.clean_up()


if __name__ == "__main__":
    main()
