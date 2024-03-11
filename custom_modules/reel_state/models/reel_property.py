from odoo import models, fields

class ReelProperty(models.Model):
    # Model name and description
    _name ='reel.property'
    # _table = 'gts_reel_property'
    _description = 'Reel Property'
    _rec_name = 'name'
    _order  = 'construction_date ASC, id ASC' # default is: id ASC

    # Python properties translated as SQL fields (Schema properties)
    name = fields.Char('Name', required=True)
    construction_date = fields.Date(string='Construction Date', required=True, default=fields.Date.today())
    area = fields.Float(string='Area')
    type = fields.Selection([('view_1', 'View 1'), ('view_2', 'View 2')], default ="view_1", string='View Type',) # dropdown

    # Relational fields
    parent_id = fields.Many2one('reel.property', string='Parent Property') # cyclic
    child_ids = fields.One2many('reel.property', 'parent_id') # cyclic
    
    room_ids = fields.One2many('reel.room', 'property_id', string='Rooms') # prop 1..1 --> rooms 0..*