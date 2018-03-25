#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
pskill: Simple cli util to kill process by it port.

Usage:
    pskill [-v|--verbose] [-c|--check] PORT
    pskill (-l | --list)
    pskill (-h | --help)

Options:
    -l --list           List all active processes.
    -v --verbose        Enable additional prints.
    -c --check          Get processes that used selected port.
    -h --help           Show this screen.

Arguments:
    PORT    Number of port to kill.
"""

from __future__ import unicode_literals

import logging

import docopt
import psutil
from tabulate import tabulate


class ProcessManager(object):
    """Manages system processes.
    """

    def __init__(self):
        self.processes = self._get_processes()

    def list(self):
        """
        :rtype: ('process_name', 'port')
        """
        return [(p[0].name(), p[1]) for p in self.processes]

    def kill_by_port(self, target_port):
        """Kill active processes that use port.
        :return: Names of killed processes.
        """
        killed = list()
        for proc, port in self.processes:
            if port == target_port:
                proc.kill()
                killed.append(proc.name())
        return killed

    def _get_processes(self):
        """
        :return: List of active processes and their ports.
        :rtype: [(psutil.Process, int)]
        """
        processes = list()
        for conn in psutil.net_connections():
            proc = psutil.Process(conn.pid)
            processes.append((proc, conn.laddr.port))
        return processes


def run():
    """Main entry point."""
    args = docopt.docopt(__doc__)

    # Process manager context
    pm = ProcessManager()

    # List active processes and exit
    if args['--list']:
        print(tabulate(pm.list(), ('name', 'port')))
        return

    # Work with port
    assert args['PORT']
    port = int(args['PORT'])

    # Activate debug prints
    if args['--verbose']:
        logging.basicConfig(level=logging.INFO, format='')

    # Show processes using this port and exit
    if args['--check']:
        using = [p[0] for p in pm.list() if p[1] == port]
        if using:
            print(''.join(using))
        else:
            logging.info('There are no processes on %d' % port)
        return

    # Kill processes on this port
    killed = pm.kill_by_port(port)
    if killed:
        logging.info('Killed: %s.' % ''.join(killed))
    else:
        logging.info("Can't found processes on %d." % port)


if __name__ == '__main__':
    run()
