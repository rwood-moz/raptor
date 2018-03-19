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

from raptor.control_server import start_control_server
from raptor.prefs import preferences
from raptor.browser import start_browser


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
        self.control_server = start_control_server()

    def run_test(self):
        binary = '/Users/rwood/mozilla-unified/obj-x86_64-apple-darwin17.4.0/dist/Nightly.app/Contents/MacOS/firefox'
        start_browser(binary, self.profile.profile)


    def clean_up(self):
        self.log.info("todo: cleanup here like delete the profile")


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    commandline.add_logging_group(parser)

    args = parser.parse_args()
    log = commandline.setup_logging('raptor', args, {'tbpl': sys.stdout})

    raptor = Raptor()

    raptor.create_profile()
    raptor.set_browser_prefs()
    raptor.install_webext()
    raptor.start_control_server()
    raptor.run_test()
    raptor.clean_up()


if __name__ == "__main__":
    main()