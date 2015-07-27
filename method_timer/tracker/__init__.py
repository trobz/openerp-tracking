# -*- coding: utf-8 -*-

import re
from openerp.tools import config

from openerp.addons.method_timer.connector import connector_factory
from openerp.addons.method_timer.tracker import tracker


def create_agent():
    """Create the global, shared tracker object."""

    connector_name = config.get('tracker_connector', 'log')
    connector_class = connector_factory.get(connector_name)

    def get_connector_args(config, pattern):
        kw = {}
        extract_args = re.compile('%s_(?P<named_arg>.*)$' % pattern)
        for option, value in config.options.iteritems():
            match = extract_args.search(option)
            if match:
                kw[match.group('named_arg')] = value
        return kw

    connector = connector_class(**get_connector_args(
        config, 'tracker_connector_%s' % connector_name))

    tracker.agent = tracker.Tracker(connector=connector)
