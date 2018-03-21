# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import

from mozlog import get_proxy_logger
from mozprofile import Profile

LOG = get_proxy_logger(component='profile')


def create_profile(browser):
    if browser == 'firefox':
        LOG.info("Created Firefox browser profile:")
        new_profile = Profile()
        LOG.info(new_profile.profile)
        return new_profile
    elif browser == 'chrome':
        LOG.info('todo: create profile on chrome')
    else:
        LOG.critical('abort: unsupported browser')
