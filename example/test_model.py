from odoo import models, fields

class TestModel(models.Model):

    # Model inherited properties(common properties)
    _name = 'test.model' # key
    _description = 'Test Model'
    _order = 'name DESC, age, id'

    # Fields schema properties
    name = fields.Char()
    age = fields.Integer()

    vendor_id = fields.Many2one('res.partner', string='Vendor')
    customer_ids = fields.Many2many('res.partner', string='Customer')

    def method_a(self):
        return ', '.join(record.name for record in self)
    
    @classmethod
    def method_b(cls):
        return cls._name