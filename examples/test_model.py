from odoo import models, fields

class TestModel(models.Model):

    # Model inherited properties
    _name = 'test.model'
    _description = 'Test Model'

    # Fields schema properties
    name = fields.Char()

    def method_a(self):
        return self.name
    
    @classmethod
    def method_b(cls):
        return cls._name