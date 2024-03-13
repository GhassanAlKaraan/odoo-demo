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
    
    
    landlord_id = fields.Many2one('res.partner', string='Landlord', required=True)
    # Logical fields, computed on the flight, not saved in db
    landlord_phone = fields.Char(related='landlord_id.phone', store=True, readonly=False)
    landlord_email = fields.Char(related='landlord_id.email', store=True, readonly=False)
    
    
    
    construction_date = fields.Date(string='Construction Date', required=True, default=fields.Date.today())
    area = fields.Float(string='Area')
    type = fields.Selection([('view_1', 'View 1'), ('view_2', 'View 2')], default ="view_1", string='View Type',) # dropdown

    # Relational fields

    # Cyclic relationship: prop can be a building parent of another prop apartment
    parent_id = fields.Many2one('reel.property', string='Parent Property')
    child_ids = fields.One2many('reel.property', 'parent_id')
    
    room_ids = fields.One2many(comodel_name='reel.room', inverse_name='property_id', string='Rooms', domain=[('type', 'in', ['bedroom', 'bathroom', 'kitchen'])], limit=3) # prop 1..1 --> rooms 0..*

    # No need for a new model. We'll use existing model: res.partner
    # tenant_ids = fields.Many2many('res.partner', string='Tenants') # prop 1..* --> tenants 0..*
    # investor_ids = fields.Many2many(comodel_name='res.partner', relation='property_investors_rel', column1='property_id', column2='investor_id', string='Investors') # prop 1..* --> investors 0..*
    
    tag_ids = fields.Many2many('reel.tag', string='Tags')