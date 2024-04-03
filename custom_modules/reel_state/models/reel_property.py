from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND, OR


class ReelProperty(models.Model):
    # Model name and description
    _name = 'reel.property'

    _sql_constraints = [  # List of tuples
        ('name_unique', 'UNIQUE(name)', 'Property name must be unique!'),
        # ('area_positive', 'CHECK(area > 0)', 'Property area must be positive')
    ]

    rental_percentage = fields.Float(string='Rental Percentage', default=0.0)
    rental_average_hours = fields.Float(string='Rental Average Hours', default=0.0)

    # _table = 'gts_reel_property'
    _description = 'Reel Property'
    _rec_name = 'name'
    _order = 'construction_date ASC, id ASC'  # default is: id ASC

    # Python properties translated as SQL fields (Schema properties)
    name = fields.Char('Name', required=True)

    landlord_id = fields.Many2one('res.partner', string='Landlord', required=False)
    # Logical fields, computed on the flight, not saved in db
    landlord_phone = fields.Char(related='landlord_id.phone', store=True, readonly=False)
    landlord_email = fields.Char(related='landlord_id.email', store=True, readonly=False)

    # compute takes a function
    landlord_info = fields.Char(compute="_compute_landlord_info",
                                inverse="_inverse_landlord_info")  # no need for (, store=True, readonly=False) when you have compute and inverse together
    number_of_properties = fields.Integer(compute="_compute_number_of_properties",
                                          search="_search_number_of_properties")

    # No idea what's going on here
    def __init__(self, env, ids, prefetch_ids):
        super().__init__(env, ids, prefetch_ids)

    def _search_number_of_properties(self, operator, value):
        property_groups = self.env['reel.property'].read_group([], ['landlord_id', '__count'], ['landlord_id'])

        def _apply_operator(count):
            return eval(f"{count} {operator} {value}")

        landlords = [group['landlord_id'][0] for group in property_groups if
                     _apply_operator(group['landlord_id_count'])]
        return [('landlord_id', 'in', landlords)]

    @api.depends('landlord_id.name', 'landlord_phone')
    def _compute_landlord_info(self):
        for record in self:  # to avoid singleton errors, loop through all records
            record.landlord_info = f"{record.landlord_id.name} ({record.landlord_phone})"

    @api.depends('landlord_id')
    def _compute_number_of_properties(self):
        # the number is dynamic, cant be assigned to a single property, we cant store it
        for record in self:
            record.number_of_properties = self.env['reel.property'].search_count(
                [('landlord_id', '=', record.landlord_id.id)])

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

    area = fields.Float(string='Area', compute="_compute_area", store=True, readonly=True)

    @api.depends('room_ids.area')
    def _compute_area(self):
        for record in self:
            record.area = sum([room.area for room in record.room_ids])
            # record.area = sum(record.room_ids.mapped('area')) # alternative

    type = fields.Selection([('view_1', 'View 1'), ('view_2', 'View 2')], default="view_1",
                            string='View Type', )  # dropdown

    # Relational fields

    # Cyclic relationship: prop can be a building parent of another prop apartment
    parent_id = fields.Many2one('reel.property', string='Parent Property')
    child_ids = fields.One2many('reel.property', 'parent_id')

    room_ids = fields.One2many(comodel_name='reel.room', inverse_name='property_id', string='Rooms',
                               domain=[('type', 'in', ['bedroom', 'bathroom', 'kitchen'])],
                               limit=3)  # prop 1..1 --> rooms 0..*

    tag_ids = fields.Many2many('reel.tag', string='Tags')

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    age = fields.Float(compute="_compute_age", store=False)  # Cannot store in db, because it's a dynamic value

    room_count = fields.Integer(compute="_compute_room_count", store=False)

    status = fields.Selection(
        [
            ('available', 'Available'),
            ('rented', 'Rented'),
            ('maintenance', 'Maintenance'),

        ], default='available', string='Status'
    )

    @api.depends('room_ids')
    def _compute_room_count(self):
        for record in self:
            record.room_count = len(record.room_ids)

    def test_search(self):
        print(self.search([('number_of_properties', '>=', 2)]))

    # fields.Date.today() is a dynamic value
    @api.depends('construction_date')
    def _compute_age(self):
        for record in self:  # Do this when it's a computed field. odoo orm way of doing things
            record.age = (fields.Date.today() - record.construction_date).days / 365

    def test_search_method(self):
        # self.method_a()

        domain_c = AND([
            [('country_id.code', 'in', ['US', 'FR'])],
            [('zip', '=', 0000)]
        ])
        # same as:
        # domain_c = ['&', ('country_id.code', 'in', ['US', 'FR']), ('zip', '=', 0000)]
        domain_b = ['&', ('name', '=', 'Property 101'), ('age', '>=', 46)]
        domain_a = [('type', '=', 'view_1')]

        # self.search(
        # [
        #     '|',  '|', ('type', '=', 'view_1'),
        #     '&', ('name', '=', 'Property 101'), ('age', '>=', 46),
        #     '&', ('country_id.code', 'in', ['US', 'FR']), ('zip', '=', 0000),
        # ]
        # )
        final_domain = OR([domain_a, domain_b, domain_c])
        self.search(final_domain)

    # def method_a(self):
    #     print("Language in method A: " + self._context.get('lang'))
    #     new_self = self.with_context(lang='fr_FR')
    #     new_self.method_b()
    #     print("Again in method A: " + self._context.get('lang'))
    #     print("New self in method A: " + new_self._context.get('lang'))
    #
    # def method_b(self):
    #     print("Language in method B: " + self._context.get('lang'))
    #     self.method_c()
    #
    # def method_c(self):
    #     print("Language in method C: " + self._context.get('lang'))

    # context is dictionary of useful key-value pairs

    @staticmethod
    def action_call_python():
        print("Python Method Button")

    # Only in python you can define dynamic domains
    # def action_view_rooms(self):
    #     action = self.env.ref('reel_state.reel_room_action').read()[0]
    #     action['domain'] = [('property_id', '=', self.ids[0])]  # self.id is not available for some reason
    #     return action

    def action_view_rooms(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rooms',
            'view_mode': 'tree,form',
            'res_model': 'reel.room',
            'domain': [('property_id', '=', self.ids[0])],
            'context': {
                'create': 0,
                'edit': 0,
                'delete': 0
            }
        }

    def action_create_room(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Room',
            'view_mode': 'tree,form',
            'res_model': 'reel.room',
            'domain': [('property_id', '=', self.ids[0])],
            'context': {
                'default_property_id': self.ids[0]
            }
        }

    def action_available(self):
        self.write({'status': 'available'})

    def action_rented(self):
        self.write({'status': 'rented'})

    def action_maintenance(self):
        self.write({'status': 'maintenance'})
