#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import json
import os
import sys
import time

from manifestparser import TestManifest
from mozlog import commandline, get_default_logger
from mozprofile import create_profile
from mozrunner import runners

from raptor.cmdline import parse_args
from raptor.control_server import RaptorControlServer
from raptor.gen_test_url import gen_test_url
from raptor.outputhandler import OutputHandler
from raptor.manifest import get_raptor_test_list
from raptor.webext import install_webext

here = os.path.abspath(os.path.dirname(__file__))
webext_dir = os.path.join(os.path.dirname(here), 'webext')


class Raptor(object):
    """Container class for Raptor"""

    def __init__(self, app, binary):
        self.raptor_venv = os.path.join(os.getcwd(), 'raptor-venv')
        self.log = get_default_logger(component='raptor')

        self.control_server = None
        self.app = app

        # Create the profile
        pref_file = os.path.join(here, 'preferences', '{}.json'.format(self.app))
        prefs = {}
        if os.path.isfile(pref_file):
            with open(pref_file, 'r') as fh:
                prefs = json.load(fh)

        try:
            self.profile = create_profile(self.app, preferences=prefs)
        except NotImplementedError:
            self.profile = None

        # Create the runner
        cmdargs = []
        if app == 'chrome':
            cmdargs.append('--load-extension={}'.format(
                           os.path.join(webext_dir, 'raptor-chrome')))

        self.output_handler = OutputHandler()
        process_args = {
            'processOutputLine': [self.output_handler],
        }
        runner_cls = runners[app]
        self.runner = runner_cls(
            binary, cmdargs=cmdargs, profile=self.profile, process_args=process_args)

    def start_control_server(self):
        self.control_server = RaptorControlServer()
        self.control_server.start()

    def run_test(self, test, timeout=None):
        gen_test_url(self.app, test)
        install_webext(self.app, self.profile)
        self.runner.start()
        first_time = int(time.time()) * 1000
        proc = self.runner.process_handler
        self.output_handler.proc = proc

        try:
            self.runner.wait(timeout)
        finally:
            try:
                self.runner.check_for_crashes()
            except NotImplementedError:  # not implemented for Chrome
                pass

        if self.runner.is_running():
            self.log("Application timed out after {} seconds".format(timeout))
            self.runner.stop()

        proc.output.append(
            "__startBeforeLaunchTimestamp%d__endBeforeLaunchTimestamp"
            % first_time)
        proc.output.append(
            "__startAfterTerminationTimestamp%d__endAfterTerminationTimestamp"
            % (int(time.time()) * 1000))

    def process_results(self):
        self.log.info('todo: process results and dump in PERFHERDER_JSON blob')
        self.log.info('- or - do we want the control server to do that?')

    def clean_up(self):
        self.control_server.stop()
        self.runner.stop()
        self.log.info("done")


def main(args=sys.argv[1:]):
    args = parse_args()
    commandline.setup_logging('raptor', args, {'tbpl': sys.stdout})
    LOG = get_default_logger(component='main')

    # if a test name specified on command line, and it exists, just run that one
    # otherwise run all available raptor tests that are found for this browser
    raptor_test_list = get_raptor_test_list(args)
    LOG.info("raptor tests scheduled to run:")
    LOG.info(raptor_test_list)

    raptor = Raptor(args.app, args.binary)

    raptor.start_control_server()

    for next_test in raptor_test_list:
        raptor.run_test(next_test)

    raptor.process_results()
    raptor.clean_up()


if __name__ == "__main__":
    main()
