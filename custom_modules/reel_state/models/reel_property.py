from odoo import models, fields

class ReelProperty(models.Model):
    # Model name and description
    _name ='reel.property'
    _description = 'Reel State Management Software'

    # Python properties translated as SQL fields (Schema properties)
    name = fields.Char('Name', required=True)
    construction_date = fields.Date(string='Construction Date', required=True, default=fields.Date.today())
    area = fields.Float(string='Area')