from odoo import models, fields


class Product(models.Model):
    #
    #
    # extend a new model, I don't want to create a new one.
    _name = 'product.product'
    _description = 'Flower Shop Product'
    _inherit = 'product.product'   # sale --> product --> product variant
    flower_id = fields.Many2one(comodel_name='flower_shop.flower', string="Flower Id")
    #
    #
    #
    is_a_flower = fields.Boolean(string='Is a Flower?')
