# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import

import time

from mozlog import get_proxy_logger

LOG = get_proxy_logger(component='browser_preferences')

# Set places maintenance far in the future (the maximum time possible in an
# int32_t) to avoid it kicking in during tests. The maintenance can take a
# relatively long time which may cause unnecessary intermittents and slow
# things down. This, like many things, will stop working correctly in 2038.
FAR_IN_FUTURE = 2147483647


def browser_prefs(browser):
    if browser == 'firefox':
        return {
            'app.update.enabled': False,
            'browser.addon-watch.interval': -1,  # Deactivate add-on watching
            'browser.aboutHomeSnippets.updateUrl':
                'https://127.0.0.1/about-dummy/',
            'browser.bookmarks.max_backups': 0,
            'browser.cache.disk.smart_size.enabled': False,
            'browser.cache.disk.smart_size.first_run': False,
            'browser.chrome.dynamictoolbar': False,
            'browser.dom.window.dump.enabled': True,
            'browser.EULA.override': True,
            'browser.link.open_newwindow': 2,
            'browser.reader.detectedFirstArticle': True,
            'browser.shell.checkDefaultBrowser': False,
            'browser.warnOnQuit': False,
            'browser.tabs.remote.autostart': False,
            'dom.allow_scripts_to_close_windows': True,
            'dom.disable_open_during_load': False,
            'dom.disable_window_flip': True,
            'dom.disable_window_move_resize': True,
            'dom.max_chrome_script_run_time': 0,
            'dom.max_script_run_time': 0,
            'extensions.autoDisableScopes': 10,
            'extensions.checkCompatibility': False,
            'extensions.enabledScopes': 5,
            'extensions.update.notifyUser': False,
            'hangmonitor.timeout': 0,
            'network.proxy.http': 'localhost',
            'network.proxy.http_port': 80,
            'network.proxy.type': 1,
            # Bug 1383896 - reduces noise in tests
            'idle.lastDailyNotification': int(time.time()),
            'places.database.lastMaintenance': FAR_IN_FUTURE,
            'security.enable_java': False,
            'security.fileuri.strict_origin_policy': False,
            'dom.send_after_paint_to_content': True,
            'security.turn_off_all_security_so_that_viruses_can_'
            'take_over_this_computer': True,
            'browser.newtabpage.activity-stream.default.sites': '',
            'browser.newtabpage.activity-stream.telemetry': False,
            'browser.newtabpage.activity-stream.tippyTop.service.endpoint': '',
            'browser.newtabpage.activity-stream.feeds.section.topstories': False,
            'browser.newtabpage.activity-stream.feeds.snippets': False,
            'browser.safebrowsing.downloads.remote.url':
                'http://127.0.0.1/safebrowsing-dummy/downloads',
            'browser.safebrowsing.provider.google.gethashURL':
                'http://127.0.0.1/safebrowsing-dummy/gethash',
            'browser.safebrowsing.provider.google.updateURL':
                'http://127.0.0.1/safebrowsing-dummy/update',
            'browser.safebrowsing.provider.google4.gethashURL':
                'http://127.0.0.1/safebrowsing4-dummy/gethash',
            'browser.safebrowsing.provider.google4.updateURL':
                'http://127.0.0.1/safebrowsing4-dummy/update',
            'browser.safebrowsing.provider.mozilla.gethashURL':
                'http://127.0.0.1/safebrowsing-dummy/gethash',
            'browser.safebrowsing.provider.mozilla.updateURL':
                'http://127.0.0.1/safebrowsing-dummy/update',
            'privacy.trackingprotection.introURL':
                'http://127.0.0.1/trackingprotection/tour',
            'browser.safebrowsing.phishing.enabled': False,
            'browser.safebrowsing.malware.enabled': False,
            'browser.safebrowsing.blockedURIs.enabled': False,
            'browser.safebrowsing.downloads.enabled': False,
            'browser.safebrowsing.passwords.enabled': False,
            'plugins.flashBlock.enabled': False,
            'privacy.trackingprotection.annotate_channels': False,
            'privacy.trackingprotection.enabled': False,
            'privacy.trackingprotection.pbmode.enabled': False,
            'browser.search.isUS': True,
            'browser.search.countryCode': 'US',
            'browser.search.geoip.url': '',
            'browser.urlbar.userMadeSearchSuggestionsChoice': True,
            'extensions.update.url':
                'http://127.0.0.1/extensions-dummy/updateURL',
            'extensions.update.background.url':
                'http://127.0.0.1/extensions-dummy/updateBackgroundURL',
            'extensions.blocklist.enabled': False,
            'extensions.blocklist.url':
                'http://127.0.0.1/extensions-dummy/blocklistURL',
            'extensions.hotfix.url':
                'http://127.0.0.1/extensions-dummy/hotfixURL',
            'extensions.update.enabled': False,
            'extensions.webservice.discoverURL':
                'http://127.0.0.1/extensions-dummy/discoveryURL',
            'extensions.getAddons.get.url':
                'http://127.0.0.1/extensions-dummy/repositoryGetURL',
            'extensions.getAddons.getWithPerformance.url':
                'http://127.0.0.1/extensions-dummy'
                '/repositoryGetWithPerformanceURL',
            'extensions.getAddons.search.browseURL':
                'http://127.0.0.1/extensions-dummy/repositoryBrowseURL',
            'media.gmp-manager.url':
                'http://127.0.0.1/gmpmanager-dummy/update.xml',
            'media.gmp-manager.updateEnabled': False,
            'extensions.systemAddon.update.url':
                'http://127.0.0.1/dummy-system-addons.xml',
            'app.normandy.api_url':
                'https://127.0.0.1/selfsupport-dummy/',
            'browser.ping-centre.staging.endpoint':
                'https://127.0.0.1/pingcentre/dummy/',
            'browser.ping-centre.production.endpoint':
                'https://127.0.0.1/pingcentre/dummy/',
            'media.navigator.enabled': True,
            'media.peerconnection.enabled': True,
            'media.navigator.permission.disabled': True,
            'media.capturestream_hints.enabled': True,
            'browser.contentHandlers.types.0.uri': 'http://127.0.0.1/rss?url=%s',
            'browser.contentHandlers.types.1.uri': 'http://127.0.0.1/rss?url=%s',
            'browser.contentHandlers.types.2.uri': 'http://127.0.0.1/rss?url=%s',
            'browser.contentHandlers.types.3.uri': 'http://127.0.0.1/rss?url=%s',
            'browser.contentHandlers.types.4.uri': 'http://127.0.0.1/rss?url=%s',
            'browser.contentHandlers.types.5.uri': 'http://127.0.0.1/rss?url=%s',
            'identity.fxaccounts.auth.uri': 'https://127.0.0.1/fxa-dummy/',
            'datareporting.healthreport.documentServerURI':
                'http://127.0.0.1/healthreport/',
            'datareporting.policy.dataSubmissionPolicyBypassNotification': True,
            'general.useragent.updates.enabled': False,
            'browser.webapps.checkForUpdates': 0,
            'browser.search.geoSpecificDefaults': False,
            'browser.snippets.enabled': False,
            'browser.snippets.syncPromo.enabled': False,
            'toolkit.telemetry.server': 'https://127.0.0.1/telemetry-dummy/',
            'experiments.manifest.uri':
                'https://127.0.0.1/experiments-dummy/manifest',
            'network.http.speculative-parallel-limit': 0,
            'lightweightThemes.selectedThemeID': "",
            'devtools.chrome.enabled': False,
            'devtools.debugger.remote-enabled': False,
            'devtools.theme': "light",
            'devtools.timeline.enabled': False,
            'identity.fxaccounts.migrateToDevEdition': False,
            'plugin.state.flash': 0,
            'media.libavcodec.allow-obsolete': True,
            'extensions.legacy.enabled': True,
            'xpinstall.signatures.required': False,
            'dom.performance.time_to_non_blank_paint.enabled': True
        }
    elif browser == 'chrome':
        # currently there are none required
        pass
    else:
        LOG.critical("abort: unsupported browser")


def set_browser_prefs(browser, profile):
    prefs_to_set = browser_prefs(browser)
    if browser == 'firefox':
        LOG.info("Setting Firefox browser preferences")
        profile.set_preferences(prefs_to_set)
    elif browser == 'chrome':
        # currently none required on chrome
        return
    else:
        LOG.critical('abort: unsupported browser')
