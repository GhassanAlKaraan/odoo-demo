from odoo import models, fields, api
from collections import defaultdict

class Product(models.Model):
    #
    #
    # extend a new model, I don't want to create a new one.
    _name = 'product.product'
    _description = 'Flower Shop Product'
    _inherit = 'product.product'  # sale --> product --> product variant
    flower_id = fields.Many2one(comodel_name='flower_shop.flower', string="Flower Id")
    #
    #
    #
    is_a_flower = fields.Boolean(string='Is a Flower?')
    #
    #
    #
    # needs_watering = fields.Boolean(compute='_compute_needs_watering', string='Needs Watering?')
    #
    # @api.depends('flower_id')
    # def _compute_needs_watering(self):
    #     for product in self:
    #         needs_water = False
    #         if product.flower_id and product.is_a_flower:
    #             lots = self.env['stock.lot'].search([('product_id', '=', product.id), ('is_a_flower', '=', True)])
    #             for lot in lots:
    #                 if lot.flower_water_ids:
    #                     last_watering = max(lot.flower_water_ids.mapped('date'))
    #                     if (fields.Date.today() - last_watering).days >= lot.product_id.flower_id.watering_frequency:
    #                         needs_water = True
    #                         break
    #         product.needs_watering = needs_water
    #
    #
    #
    needs_watering = fields.Boolean(string='Needs Watering', default=False)

    def action_needs_watering(self):
        from datetime import timedelta
        today = fields.Date.today()
        flowers = self.search([('is_a_flower', '=', True)])
        flower_serials = self.env['stock.lot'].search([('product_id', 'in', flowers.ids)])
        lot_vals = defaultdict(bool)

        for serial in flower_serials:
            if serial.flower_water_ids:
                last_watered_date = max(serial.flower_water_ids.mapped('date'))
                frequency = serial.product_id.flower_id.watering_frequency
                needs_watering = (today - last_watered_date) >= timedelta(days=frequency)
                lot_vals[serial.product_id.id] |= needs_watering
            else:
                lot_vals[serial.product_id.id] = True

        for flower in flowers:
            flower.needs_watering = lot_vals[flower.id]