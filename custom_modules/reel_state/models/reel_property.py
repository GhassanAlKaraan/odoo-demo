from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ReelProperty(models.Model):
    # Model name and description
    _name ='reel.property'
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property name must be unique!')
    ]
    
    
    # _table = 'gts_reel_property'
    _description = 'Reel Property'
    _rec_name = 'name'
    _order  = 'construction_date ASC, id ASC' # default is: id ASC

    # Python properties translated as SQL fields (Schema properties)
    name = fields.Char('Name', required=True)
    
    
    landlord_id = fields.Many2one('res.partner', string='Landlord', required=True)
    # Logical fields, computed on the flight, not saved in db
    # Not stored + ReadOnly
    landlord_phone = fields.Char(related='landlord_id.phone', store=True, readonly=False)
    landlord_email = fields.Char(related='landlord_id.email', store=True, readonly=False)
    
    # compute takes a function
    landlord_info = fields.Char(compute="_compute_landlord_info", inverse="_inverse_landlord_info") # no need for (, store=True, readonly=False) when you have compute and inverse together
    number_of_properties = fields.Integer(compute="_compute_number_of_properties", search="_search_number_of_properties")
    
    def test_search(self):
        print(self.search([('number_of_properties', '>=', 2)]))
    
    def _search_number_of_properties(self, operator, value):
        property_groups = self.env['reel.property'].read_group([], ['landlord_id', '__count'], ['landlord_id'])

        def _apply_operator(count):
            return eval(f"{count} {operator} {value}")
        landlords = [group['landlord_id'][0] for group in property_groups if _apply_operator(group['landlord_id_count'])]
        return [('landlord_id', 'in', landlords)]
    
    @api.depends('landlord_id.name', 'landlord_phone')
    def _compute_landlord_info(self):
        for record in self: # to avoid singleton errors, loop through all records
            record.landlord_info = f"{record.landlord_id.name} ({record.landlord_phone})"
    
    @api.depends('landlord_id')
    def _compute_number_of_properties(self): # the number is dynamic, cant be assigned to a single property, we cant store it
        for record in self:
            record.number_of_properties = self.env['reel.property'].search_count([('landlord_id', '=', record.landlord_id.id)])
    
    def _inverse_landlord_info(self):
        for record in self:
            record.landlord_id.name = record.landlord_info.split(' ')[0]
            record.landlord_phone = record.landlord_info.split(' ')[1].strip('()')
    
    construction_date = fields.Date(string='Construction Date', required=True, default=fields.Date.today())
    
    @api.constrains('construction_date')
    def _constrain_construction_date(self):
        for record in self: 
            if record.construction_date > fields.Date.today():
                raise ValidationError("Construction date cannot be in the future")
    
    
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
    
    # @api.onchange('landlord_phone')
    # def _onchange_landlord_phone(self):
    #     if not self.landlord_phone:
    #         raise UserError("Landlord phone is required") # odoo rolls back any changes here

    @api.onchange('landlord_phone')
    def _has_onchange_landlord_phone(self, field):
        self.name += self.landlord_phone or ''