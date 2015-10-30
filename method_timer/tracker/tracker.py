# -*- coding: utf-8 -*-

import logging
from time import time

# shared tracker agent instance
agent = None
_logger = logging.getLogger('method_timer')


class Tracker(object):

    def __init__(self, connector):
        _logger.info('method_timer agent instantiated with %s connector',
                     connector.__class__.__name__)
        self.connector = connector
        self.configured = False

    def configure(self, callee, warning, critical):
        """
        Configure thresholds once
        """
        if not self.configured:
            self.connector.configure(callee.__module__, callee.__name__,
                                     warning, critical)
            self.configured = True

    def record(self, callee, args, kw, warning=None, critical=None):
        """
        Record the execution time of a method
        """
        start = time()
        result = callee(*args, **kw)
        self.connector.add(callee.__module__, callee.__name__, start, time())
        return result