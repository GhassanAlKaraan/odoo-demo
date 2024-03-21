from odoo import api, SUPERUSER_ID
from . import models, wizards

def _my_custom_uninstall_method(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].search([], limit=5, order='id DESC').write({
        'name': 'Updated from Uninstall hook'
    })

def _my_custom_post_method(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].search([], offset=5, limit=5, order='id DESC').write({
        'name': 'Updated from Post hook'
    })

def _my_custom_pre_method(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].search([], offset=10, limit=5, order='id DESC').write({
        'name': 'Updated from Pre hook'
    })