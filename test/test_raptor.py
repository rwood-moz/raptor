from __future__ import absolute_import, unicode_literals

import os

import pytest
from mozprofile import Profile

from raptor.control_server import RaptorControlServer
from raptor.raptor import Raptor


@pytest.mark.parametrize('app', ['firefox', 'chrome', 'unknown'])
def test_create_profile(options, app, get_prefs):
    options['app'] = app
    raptor = Raptor(**options)

    if app != 'firefox':
        assert raptor.profile is None
        return

    assert isinstance(raptor.profile, Profile)
    # This pref is set in mozprofile
    firefox_pref = 'user_pref("app.update.enabled", false);'
    # This pref is set in raptor
    raptor_pref = 'user_pref("security.enable_java", false);'

    prefs_file = os.path.join(raptor.profile.profile, 'user.js')
    with open(prefs_file, 'r') as fh:
        prefs = fh.read()
        assert firefox_pref in prefs
        assert raptor_pref in prefs


def test_start_and_stop_server(raptor):
    assert raptor.control_server is None

    raptor.start_control_server()
    assert isinstance(raptor.control_server, RaptorControlServer)

    assert raptor.control_server._server_thread.is_alive()
    raptor.clean_up()
    assert not raptor.control_server._server_thread.is_alive()


@pytest.mark.parametrize('app', [
    'firefox',
    pytest.mark.xfail('chrome'),
])
def test_start_browser(get_binary, app):
    binary = get_binary(app)
    assert binary

    raptor = Raptor(app, binary)
    raptor.start_control_server()

    # TODO We can't run the browser just yet because there is no
    # easy way to control the process from a raptor instance. This
    # will be fixed soon.
    # test = 'raptor-{}-tp7'.format(app)
    # raptor.run_test(test)
    raptor.clean_up()
