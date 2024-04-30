from odoo import fields, models, api
from odoo.exceptions import ValidationError, AccessError


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

    @api.depends('product_id.is_a_flower')
    def _compute_is_a_flower(self):
        for lot in self:
            lot.is_a_flower = lot.product_id.is_a_flower

    def action_flower_water(self):

        # Only for Gardeners
        if not self.env.user.has_group('flower_shop.group_gardeners'):
            raise AccessError("Only users with the gardener group can water the plants.")

        for lot in self.filtered('is_a_flower'):
            if lot.flower_water_ids:
                last_watering = max(lot.flower_water_ids.mapped('date'))
                if (fields.Date.today() - last_watering).days >= lot.product_id.flower_id.watering_frequency:
                    self.env['flower_shop.flower.water'].create({'serial_number': lot.id})
                else:
                    raise ValidationError("Wait a bit longer before watering again.")
            else:
                self.env['flower_shop.flower.water'].create({'serial_number': lot.id})

    @api.constrains('flower_water_ids')
    def _check_watering_frequency(self):
        for record in self:
            if record.flower_water_ids:
                last_watering = max(record.flower_water_ids.mapped('date'))
                if (fields.Date.today() - last_watering).days < record.product_id.flower_id.watering_frequency:
                    raise ValidationError("Wait a bit longer before watering again.")

    def action_open_watering_times(self):
        self.ensure_one()  # Ensure that the method is called on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Water Records',
            'view_mode': 'tree,form',
            'res_model': 'flower_shop.flower.water',
            'domain': [('serial_number', '=', self.ids[0])],
            'context': {'default_serial_number': self.ids[0]},
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env["product.product"].browse(vals["product_id"])
            if product.sequence_id:
                vals["name"] = product.sequence_id.next_by_id()
        return super().create(vals_list)
