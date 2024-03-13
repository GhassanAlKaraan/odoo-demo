from odoo import models, fields


class ReelTag(models.Model):
    _name ='reel.tag'
    _description = 'Reel Tag'
    
    name = fields.Char('Name', required=True)
    color = fields.Integer(string='Color Index', required=True)