from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime


class Product(models.Model):
    # _name = 'product.product'
    # _description = 'Flower Shop Product'
    _inherit = 'product.product'  # sale --> product --> product variant
    flower_id = fields.Many2one(comodel_name='flower_shop.flower', string="Flower Id")
    is_a_flower = fields.Boolean(string='Is a Flower?')

    needs_watering = fields.Boolean(string='Needs Watering', default=False)

    # this function just solves an error at creation: ensures that write_date is always a datetime object
    def _compute_write_date(self):
        for record in self:
            product_write_date = record.write_date if record.write_date else datetime.min
            template_write_date = record.product_tmpl_id.write_date if record.product_tmpl_id.write_date else datetime.min
            record.write_date = max(product_write_date, template_write_date)

    def action_needs_watering(self):
        today = fields.Date.today()
        flowers = self.search([('is_a_flower', '=', True)])
        flower_serials = self.env['stock.lot'].search([('product_id', 'in', flowers.ids)])
        lot_vals = defaultdict(bool)

        for serial in flower_serials:
            if serial.flower_water_ids:
                last_watered_dates = serial.flower_water_ids.mapped('date')
                if last_watered_dates:
                    last_watered_date = max(last_watered_dates)
                    frequency = serial.product_id.flower_id.watering_frequency
                    if isinstance(last_watered_date, fields.Date):
                        days_since_last_watered = (today - last_watered_date).days
                        needs_watering = days_since_last_watered >= frequency
                        lot_vals[serial.product_id.id] |= needs_watering
                else:
                    # If there are no watering records, consider that it needs watering
                    lot_vals[serial.product_id.id] = True

        for flower in flowers:
            flower.needs_watering = lot_vals[flower.id]

    sequence_id = fields.Many2one("ir.sequence", "Flower Sequence")

    gardener_ids = fields.Many2many(
        comodel_name='res.users',
        relation='product_gardener_rel',
        column1='product_id',
        column2='user_id',
        string='Gardeners'
    )
