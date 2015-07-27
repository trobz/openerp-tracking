# -*- coding: utf-8 -*-

# shared tracker agent instance
agent = None

from time import time

class Tracker(object):

    def __init__(self, connector):
        self.connector = connector

    def configure(self, callee, warning, critical):
        """
        Configure thresholds
        """
        self.connector.configure(callee.__module__, callee.__name__,
                                 warning, critical)

    def record(self, callee, args, kw, warning=None, critical=None):
        """
        Record the execution time of a method
        """
        start = time()
        result = callee(*args, **kw)
        self.connector.add(callee.__module__, callee.__name__, start, time())
        return result