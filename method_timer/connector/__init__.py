# -*- coding: utf-8 -*-

from openerp.addons.method_timer.connector.core \
    import ConnectorFactory
from openerp.addons.method_timer.connector.log_connector \
    import LogConnector
from openerp.addons.method_timer.connector.redis_connector \
    import RedisConnector

# shared connector factory
connector_factory = ConnectorFactory()
connector_factory.register('log', LogConnector)
connector_factory.register('redis', RedisConnector)
