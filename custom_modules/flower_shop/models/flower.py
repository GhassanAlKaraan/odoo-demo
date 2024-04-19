from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Flower(models.Model):
    _name = 'flower_shop.flower'
    _description = 'Flower'
    _rec_name = 'common_name'  # display name of choice

    # names
    common_name = fields.Char('Name', required=True)
    scientific_name = fields.Char('Scientific Name', required=True)

    # season
    season_start_date = fields.Date('Season Start Date', required=True)
    season_end_date = fields.Date('Season End Date', required=True)

    # control the season dates
    @api.constrains('season_start_date', 'season_end_date')
    def _check_season_dates(self):  # dates constraints
        for record in self:
            if record.season_start_date and record.season_end_date:
                if record.season_start_date > record.season_end_date:
                    raise ValidationError("The season end date must be after the season start date.")

    # watering
    watering_frequency = fields.Integer('Watering Frequency', required=True)  # once every __ days
    watering_amount = fields.Float('Watering Amount', required=True)  # amount of water in milliliters

    # api.depends ?
    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.scientific_name, flower.common_name)) for flower in self]
