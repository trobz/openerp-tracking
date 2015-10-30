# -*- coding: utf-8 -*-

import time

class Record(object):
    """
    Tracking item
    """

    def __init__(self, module, method, start_at, end_at, info=None):
        self.method = method
        self.module = module
        self.created_at = time.time()
        self.start_at = start_at
        self.end_at = end_at
        self.info = info

    def key(self):
        """
        Get record signature
        """
        return '%s:%s' % (self.module, self.method)

    def duration(self):
        """
        Calculate execution time
        """
        return self.end_at - self.start_at
