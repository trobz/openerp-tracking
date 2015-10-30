# -*- coding: utf-8 -*-

import logging

from openerp.addons.method_timer.tracker.record import Record


class Connector(object):
    """
    Abstract connector used to store action response time
    """

    def __init__(self):
        self.log = logging.getLogger('method_timer')

    def configure(self, module, method, warning, critical):
        """
        Configure thresolds
        """
        raise Exception('configure method must be implemented!')

    def add(self, module, method, start_at, end_at, info=None):
        """
        Store the tracked value
        """
        self.commit(Record(module, method, start_at, end_at, info))

    def commit(self, record):
        """
        Commit the record
        override this method to implement a storage method
        """
        raise Exception('commit method must be implemented!')


class ConnectorFactory(object):
    """
    Connector factory
    """

    con_classes = {}

    def register(self, name, con_class):
        """
        Register a connector in the factory
        """
        self.con_classes[name] = con_class

    def get(self, name):
        """
        Get a connector by name
        """
        if not self.con_classes.get(name):
            raise Exception('%s connector not found.' % name)
        return self.con_classes.get(name)
