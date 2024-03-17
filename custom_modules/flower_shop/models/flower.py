from odoo import models, fields

class Flower(models.Model):
    
    _name = 'flower'
    _description = 'Flower'
    
    common_name = fields.Char('Name', required=True)
    
    scientific_name = fields.Char('Scientific Name', required=True)
    
    season_start_date = fields.Date('Season Start Date', required=True)
    season_end_date = fields.Date('Season End Date', required=True)
    # last_watered = fields.Date('Last Watered')
    watering_frequency = fields.Integer('Watering Frequency', required=True) # once every 3 days
    watering_amount = fields.Float('Watering Amount', required=True) # amount of water in milliliters
    