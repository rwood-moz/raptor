from __future__ import absolute_import, unicode_literals

import time
from BaseHTTPServer import HTTPServer

from raptor.control_server import RaptorControlServer


def test_start_and_stop():
    control = RaptorControlServer()

    assert control.server is None
    control.start()
    assert isinstance(control.server, HTTPServer)
    assert control.server.fileno()
    assert control._server_thread.is_alive()

    control.stop()
    # XXX using sleep is generally bad, but this is pretty low risk
    time.sleep(0.1)
    assert not control._server_thread.is_alive()
