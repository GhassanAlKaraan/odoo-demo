from odoo import models, fields
from odoo.exceptions import UserError


class ResPartnerCustom(models.Model):
    _name = 'res.partner.custom'
    _inherit = 'res.partner'

    new_test_btco = fields.Integer()
    channel_ids = fields.Many2many(relation='res_partner_custom_channels_rel')

    def write(self, vals):
        raise UserError("You cannot modify a partner")


class TestModelCustom(models.Model):
    _name = 'res.partner.custom'
    _inherit = 'test.model'

    new_test_btco = fields.Integer()
    channel_ids = fields.Many2many(relation='res_partner_custom_channels_rel')

    def write(self, vals):
        raise UserError("You cannot modify a partner")
