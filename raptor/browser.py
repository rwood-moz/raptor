# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from mozlog import get_proxy_logger
from raptor_process import run_browser


LOG = get_proxy_logger(component="browser")


def start_browser(browser, browser_bin, profile):
    minidump_dir = os.getcwd()
    timeout = 10000

    if browser == 'firefox':
        command_args = [browser_bin, '--profile', profile.profile]
        LOG.info('Starting Firefox!')
        LOG.info(command_args)
    elif browser == 'chrome':
        # for chrome, add the --load-extension to the cmd line
        # temp hard code for now
        command_args = [browser_bin,
                        '--load-extension=/Users/rwood/raptor/webext/raptor-chrome']
        LOG.info('Starting Google Chrome!')
        LOG.info(command_args)
    else:
        LOG.critical("abort: unsupported browser")

    # start the browser (and on startup, the webext starts the test)
    try:
        run_browser(
            command_args,
            minidump_dir,
            timeout=timeout
        )
        # framework halts here until browser is shutdown
    except Exception:
        # self.check_for_crashes(browser_config, minidump_dir,
        #                        test_config['name'])
        raise
