#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from mozlog import get_proxy_logger
from raptor_process import run_browser


LOG = get_proxy_logger(component="run_test")


def start_browser(browser_bin, profile):
    command_args = [browser_bin, '--profile', profile]
    minidump_dir = os.getcwd()
    timeout = 10000

    LOG.info('Starting test!')
    LOG.info(command_args)

    try:
        pcontext = run_browser(
            command_args,
            minidump_dir,
            timeout=timeout
        )
    except Exception:
        #self.check_for_crashes(browser_config, minidump_dir,
        #                       test_config['name'])
        raise
