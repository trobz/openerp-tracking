# -*- coding: utf-8 -*-

import logging
from functools import wraps

from openerp.addons.method_timer.tracker import tracker

_logger = logging.getLogger('tracker')


def track(warning=None, critical=None):
    """
    tracking decorator
    warning and critical can be used to set threshold value in second
    """
    def decorator(func):
        if tracker.agent and warning or critical:
            tracker.agent.configure(func, warning, critical)

        @wraps(func)
        def wrapper(*args, **kw):
            if tracker.agent:
                _logger.debug('record %s response time', func)
                return tracker.agent.record(func, args, kw)
            else:
                _logger.debug('tracking agent not instantiated')
                return func(*args, **kw)

        return wraps(func)(wrapper)

    return decorator
