# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# originally from talos_process.py

from __future__ import absolute_import

import signal
import time
import traceback
import subprocess
from threading import Event

import mozcrash
from mozlog import get_proxy_logger
from mozprocess import ProcessHandler


LOG = get_proxy_logger(component='raptor_process')


class RaptorError(Exception):
    "Errors found while running the talos harness."


class Reader(object):
    def __init__(self, event):
        self.got_end_timestamp = False
        self.got_timeout = False
        self.event = event
        self.proc = None

    def __call__(self, line):
        if line.find('__raptor_shutdownBrowser') != -1:
            self.got_end_timestamp = True
            self.event.set()
        if not (line.startswith('JavaScript error:') or
                line.startswith('JavaScript warning:')):
            LOG.process_output(self.proc.pid, line)


def run_browser(command, minidump_dir, timeout=None, on_started=None,
                debug=None, debugger=None, debugger_args=None, **kwargs):
    """
    Run the browser using the given `command`.

    After the browser prints __endTimestamp, we give it 5
    seconds to quit and kill it if it's still alive at that point.

    Note that this method ensure that the process is killed at
    the end. If this is not possible, an exception will be raised.

    :param command: the commad (as a string list) to run the browser
    :param minidump_dir: a path where to extract minidumps in case the
                         browser hang. This have to be the same value
                         used in `mozcrash.check_for_crashes`.
    :param timeout: if specified, timeout to wait for the browser before
                    we raise a :class:`RaptorError`
    :param on_started: a callback that can be used to do things just after
                       the browser has been started. The callback must takes
                       an argument, which is the ProcessHandler instance
    :param kwargs: additional keyword arguments for the :class:`ProcessHandler`
                   instance

    Returns a mozprocess.ProcessHandler instance, with available output and pid used.
    """

    debugger_info = find_debugger_info(debug, debugger, debugger_args)
    if debugger_info is not None:
        return run_in_debug_mode(command, debugger_info,
                                 on_started=on_started, env=kwargs.get('env'))

    first_time = int(time.time()) * 1000
    wait_for_quit_timeout = 5
    event = Event()
    reader = Reader(event)

    # LOG.info("Using env: %s" % pprint.pformat(kwargs['env']))

    kwargs['storeOutput'] = True
    kwargs['processOutputLine'] = reader
    kwargs['onFinish'] = event.set
    proc = ProcessHandler(command, **kwargs)
    reader.proc = proc
    proc.run()

    LOG.process_start(proc.pid, ' '.join(command))
    try:
        # wait until we saw __endTimestamp in the proc output,
        # or the browser just terminated - or we have a timeout
        if not event.wait(timeout):
            LOG.info("Timeout waiting for test completion; killing browser...")
            # try to extract the minidump stack if the browser hangs
            mozcrash.kill_and_get_minidump(proc.pid, minidump_dir)
            raise RaptorError("timeout")
        if reader.got_end_timestamp:
            for i in range(1, wait_for_quit_timeout):
                if proc.wait(1) is not None:
                    break
            if proc.poll() is None:
                LOG.info(
                    "Browser shutdown timed out after {0} seconds, terminating"
                    " process.".format(wait_for_quit_timeout)
                )
        elif reader.got_timeout:
            raise RaptorError('Application process timed out')
    finally:
        # this also handle KeyboardInterrupt
        # ensure early the process is really terminated
        return_code = None
        try:
            return_code = proc.kill()
            if return_code is None:
                return_code = proc.wait(1)
        except Exception:
            # Maybe killed by kill_and_get_minidump(), maybe ended?
            LOG.info("Unable to kill process")
            LOG.info(traceback.format_exc())

    proc.output.append(
        "__startBeforeLaunchTimestamp%d__endBeforeLaunchTimestamp"
        % first_time)
    proc.output.append(
        "__startAfterTerminationTimestamp%d__endAfterTerminationTimestamp"
        % (int(time.time()) * 1000))

    if return_code is not None:
        LOG.process_exit(proc.pid, return_code)
    else:
        LOG.debug("Unable to detect exit code of the process %s." % proc.pid)
    return proc


def find_debugger_info(debug, debugger, debugger_args):
    debuggerInfo = None
    if debug or debugger or debugger_args:
        import mozdebug

        if not debugger:
            # No debugger name was provided. Look for the default ones on
            # current OS.
            debugger = mozdebug.get_default_debugger_name(mozdebug.DebuggerSearch.KeepLooking)

        debuggerInfo = None
        if debugger:
            debuggerInfo = mozdebug.get_debugger_info(debugger, debugger_args)

        if debuggerInfo is None:
            raise RaptorError('Could not find a suitable debugger in your PATH.')

    return debuggerInfo


def run_in_debug_mode(command, debugger_info, on_started=None, env=None):
    signal.signal(signal.SIGINT, lambda sigid, frame: None)
    command_under_dbg = [debugger_info.path] + debugger_info.args + command

    proc = subprocess.Popen(command_under_dbg, env=env)

    if on_started:
        on_started(proc)

    return_code = proc.wait()

    if return_code is not None:
        LOG.process_exit(proc.pid, return_code)
    else:
        LOG.debug("Unable to detect exit code of the process %s." % proc.pid)

    return proc
