from __future__ import absolute_import, unicode_literals

import os
import time
from argparse import Namespace
from BaseHTTPServer import HTTPServer

import pytest
from mozprofile import Profile

from raptor.raptor import Raptor


@pytest.fixture
def options():
    return Namespace(
        browser='firefox',
        browser_path='path/to/dummy/browser',
        test='test_dummy',
    )


@pytest.fixture
def raptor(options):
    return Raptor(options)


@pytest.mark.parametrize('browser', ['firefox', 'chrome', 'unknown'])
def test_create_profile(raptor, browser):
    raptor.browser = browser
    assert raptor.profile is None

    raptor.create_profile()
    if browser == 'firefox':
        assert isinstance(raptor.profile, Profile)
    else:
        assert raptor.profile is None


def test_set_preferences(raptor):
    raptor.create_profile()

    example_pref = 'user_pref("app.update.enabled", false);'
    prefs_file = os.path.join(raptor.profile.profile, 'user.js')
    with open(prefs_file, 'r') as fh:
        assert example_pref not in fh.read()

    raptor.set_browser_prefs()

    with open(prefs_file, 'r') as fh:
        assert example_pref in fh.read()


def test_set_preferences_without_profile(raptor):
    raptor.set_browser_prefs()


@pytest.mark.xfail(reason="Control server assumes os.getcwd() is where file lives")
def test_start_and_stop_server(raptor):
    assert raptor.control_server is None

    raptor.start_control_server()
    assert isinstance(raptor.control_server, HTTPServer)

    assert raptor.control_server._server_thread.is_alive()
    raptor.clean_up()
    # XXX using sleep is generally bad, but this is pretty low risk
    time.sleep(0.1)
    assert not raptor.control_server._server_thread.is_alive()


@pytest.mark.parametrize('browser', [
    pytest.mark.xfail('firefox'),
    pytest.mark.xfail('chrome'),
])
def test_start_browser(raptor, get_binary, browser):
    binary = get_binary(browser)
    raptor.browser = browser
    raptor.browser_path = binary
    raptor.create_profile()
    raptor.set_browser_prefs()
    raptor.install_webext()
    raptor.start_control_server()
    raptor.run_test()
    raptor.clean_up()
