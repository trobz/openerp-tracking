# -*- coding: utf-8 -*-

import logging

from openerp.addons.method_timer.connector.core import Connector


class LogConnector(Connector):
    """
    Log method response time with the logging facility
    """

    def __init__(self):
        super(LogConnector, self).__init__()
        self.thresholds = {}

    def configure(self, module, method, warning, critical):
        """
        Configure thresholds
        """
        self.thresholds['%s:%s' % (module, method)] = {
            'warning': warning,
            'critical': critical
        }
        self.log.info('Record method response time in log')

    def commit(self, record):
        """
        Log the record
        """
        level = logging.INFO

        th = self.thresholds.get(record.key())
        if th and th['warning'] and self.duration() > th['warning']:
            level = logging.WARNING
        if th and th['critical'] and self.duration() > th['critical']:
            level = logging.CRITICAL

        self.log.log(level, 'method %s was running during %s second(s)',
                     record.method, record.duration())
