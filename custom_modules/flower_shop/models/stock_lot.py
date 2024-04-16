from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StockLot(models.Model):
    # When it comes to manage watering, we will do so from the stock lot, don't touch the flower model
    _inherit = "stock.lot"

    # one serial numbered flower can be watered multiple times
    flower_water_ids = fields.One2many(
        comodel_name="flower_shop.flower.water",
        inverse_name="serial_number",
        string="Water Records"
    )

    # computed field
    is_a_flower = fields.Boolean(
        compute='_compute_is_a_flower',
        store=True,
        string='Is a Flower?'
    )

    @api.depends('product_id')
    def _compute_is_a_flower(self):
        for lot in self:
            lot.is_a_flower = lot.product_id.is_a_flower

    def action_flower_water(self):
        for lot in self.filtered('is_a_flower'):
            if lot.flower_water_ids:
                last_watering = max(lot.flower_water_ids.mapped('date'))
                if (fields.Date.today() - last_watering).days >= lot.product_id.flower_id.watering_frequency:
                    self.env['flower_shop.flower.water'].create({'serial_number': lot.id})
            else:
                self.env['flower_shop.flower.water'].create({'serial_number': lot.id})

    # def action_flower_water(self):
    #     # Filter out the records where is_a_flower is True
    #     flowers = self.filtered(lambda rec: rec.is_a_flower)
    #
    #     for record in flowers:
    #         # Water_ids is sorted such that the most recent watering record is first
    #         if record.water_ids:
    #             last_watered_date = record.water_ids[0].date
    #             frequency = record.product_id.flower_id.watering_frequency
    #             today_date = fields.Date.today()
    #
    #             # Calculate the difference in days between today and the last watered date
    #             if (today_date - last_watered_date).days >= frequency:
    #                 # If it's time to water again
    #                 self.env['flower_shop.flower.water'].create({
    #                     'serial_number': record.id,
    #                 })
    #         else:
    #             # If there are no watering records, we assume it needs watering
    #             self.env['flower_shop.flower.water'].create({
    #                 'serial_number': record.id,
    #             })

    @api.constrains('flower_water_ids')
    def _check_watering_frequency(self):
        for record in self:
            if record.flower_water_ids:
                last_watering = max(record.flower_water_ids.mapped('date'))
                if (fields.Date.today() - last_watering).days < record.product_id.flower_id.watering_frequency:
                    raise ValidationError("Wait a bit longer before watering again.")
