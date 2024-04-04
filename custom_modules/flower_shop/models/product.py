from odoo import models, fields


class Product(models.Model):
    #
    #
    #
    # _name = 'flower_shop.product' # Why not working???
    _name = 'product.product'
    _description = 'Flower Shop Product'
    _inherit = 'product.product'   # sale --> product --> product variant
    flower_id = fields.Many2one(comodel_name='flower_shop.flower', string="Flower Id")
    #
    #
    #
    is_a_flower = fields.Boolean(string='Is a Flower?')
