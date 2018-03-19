#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import argparse
import os
import sys
import time

from mozlog import commandline, get_default_logger
from mozprofile import Profile, AddonManager

from raptor.browser import start_browser
from raptor.cmdline import parse_args
from raptor.control_server import RaptorControlServer
from raptor.prefs import preferences


class Raptor(object):
    """Container class for Raptor"""

    def __init__(self):
        self.raptor_venv = os.path.join(os.getcwd(), 'raptor-venv')
        self.log = get_default_logger(component='raptor')
        self.control_server = None

    def create_profile(self):
        self.log.info("Creating browser profile")
        self.profile = Profile()
        self.log.info(self.profile.profile)

    def set_browser_prefs(self):
        self.log.info("Setting browser preferences")
        self.profile.set_preferences(preferences)

    def install_webext(self):
        addons = []
        here = os.path.abspath(os.getcwd())
        addons.append(os.path.join(here, 'webext', 'raptor-firefox'))
        self.log.info("Installing addons:")
        self.log.info(addons)
        self.profile.addon_manager.install_addons(addons=addons)

    def start_control_server(self):
        self.control_server = RaptorControlServer()
        self.control_server.start()

    def run_test(self, browser_path):
        start_browser(browser_path, self.profile.profile)

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
    browser = args.browser
    browser_path = args.browser_path

    log = commandline.setup_logging('raptor', args, {'tbpl': sys.stdout})

    raptor = Raptor()

    raptor.create_profile()
    raptor.set_browser_prefs()
    raptor.install_webext()
    raptor.start_control_server()
    raptor.run_test(browser_path)
    raptor.process_results()
    raptor.clean_up()


if __name__ == "__main__":
    main()