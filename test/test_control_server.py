from __future__ import absolute_import, unicode_literals

from BaseHTTPServer import HTTPServer

from mozlog.structuredlog import set_default_logger, StructuredLogger
set_default_logger(StructuredLogger('test_control_server'))

from raptor.control_server import RaptorControlServer  # noqa: E402


def test_start_and_stop():
    control = RaptorControlServer()

    assert control.server is None
    control.start()
    assert isinstance(control.server, HTTPServer)
    assert control.server.fileno()
    assert control._server_thread.is_alive()

    control.stop()
    assert not control._server_thread.is_alive()
