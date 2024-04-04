from odoo import models, fields
from odoo.exceptions import UserError


class TestModelDelegated(models.Model):
    # Delegation Inheritance. Example essentials
    _name = 'test.mode.delegated'
    _inherits = {'test.model': 'test_model_is'}

    test_model_id = fields.Many2many(comodel_name='test.model')
    #
    new_test_btco = fields.Integer()
