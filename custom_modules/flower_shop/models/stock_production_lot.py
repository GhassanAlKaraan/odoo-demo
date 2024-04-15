from odoo import fields, models


class StockProductionLot(models.Model):
    # Here we will manage the stock of the flowers, don't touch the flower model
    # when it comes to manage watering
    _inherit = "stock.lot"

    # one serial numbered flower can be watered multiple times
    # waterings
    flower_water_ids = fields.One2many(comodel_name="flower_shop.flower.water", inverse_name="serial_number")

    def action_flower_water(self):
        # Filter out the records where is_a_flower is True
        flowers = self.filtered(lambda rec: rec.is_a_flower)

        for record in flowers:
            # Water_ids is sorted such that the most recent watering record is first
            if record.water_ids:
                last_watered_date = record.water_ids[0].date
                frequency = record.product_id.flower_id.watering_frequency
                today_date = fields.Date.today()

                # Calculate the difference in days between today and the last watered date
                if (today_date - last_watered_date).days >= frequency:
                    # If it's time to water again
                    self.env['flower_shop.flower.water'].create({
                        'serial_number': record.id,
                    })
            else:
                # If there are no watering records, we assume it needs watering
                self.env['flower_shop.flower.water'].create({
                    'serial_number': record.id,
                })
