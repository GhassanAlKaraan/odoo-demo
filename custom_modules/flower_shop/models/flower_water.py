from odoo import fields, models


class FlowerWater(models.Model):
    _name = 'flower_shop.flower.water'
    _description = 'Watering Model for a Flower'

    # Order by watering date
    _order = "date desc"

    # Which flower is this?
    # You can have many watering instances of me
    serial_number = fields.Many2one("stock.lot", string="Serial Number")

    date = fields.Date("Watering Date", required=True, default=fields.Date.context_today)