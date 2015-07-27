# -*- coding: utf-8 -*-

from openerp.addons.method_timer.tracker import create_agent


def post_load():
    create_agent()
