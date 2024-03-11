from odoo import models, fields

class ReelRoom(models.Model):
    _name = 'reel_room'
    _description = 'Reel Room'

    name = fields.Char('Name', required=True)
    type = fields.Selection(
        [('bedroom','Bedroom'),
         ('bathroom','Bathroom'),
         ('kitchen','Kitchen'),
         ], default ='bedroom', required = True
    )

    property_id = fields.Many2one('reel.property', string='Property') # room 0..* --> prop 1..1