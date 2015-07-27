# -*- coding: utf-8 -*-

import redis
import json

from openerp.tools import config
from openerp.addons.method_timer.connector.core import Connector


class RedisConnector(Connector):
    """
    Store record in a Redis database
    """
    def __init__(self, host, port, db=0):
        super(RedisConnector, self).__init__()

        self.tracker_name = config.get('tracker_name')
        if not self.tracker_name:
            raise Exception('Failed to start the tracking, Odoo config ' +
                            'must contain a value for "tracker_name".')

        self.pool = redis.ConnectionPool(host=host, port=port, db=int(db))
        self.log.info('Connected to Redis on %s:%s, db: %s', host, port, db)

    def configure(self, module, method, warning, critical):
        """
        Configure thresholds on Redis
        """
        r = redis.Redis(connection_pool=self.pool)
        key = 'method_timer:meta:%s:%s:%s' % (self.tracker_name,
                                              module,
                                              method)
        r.set(key + ':warning', warning)
        r.set(key + ':critical', critical)

    def commit(self, record):
        """
        Save the record on Redis
        """
        r = redis.Redis(connection_pool=self.pool)
        key = 'method_timer:data:%s:%s:%s' % (self.tracker_name,
                                              record.module,
                                              record.method)
        data = {
            'duration': record.duration(),
            'created_at': record.created_at
        }
        r.rpush(key, json.dumps(data))
